from datetime import datetime as dt

from django.contrib.auth import login, authenticate
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import CreateView, FormView, TemplateView, UpdateView
from django.contrib import messages

from odalc.base.models import Course, CourseAvailability
from odalc.base.views import UserDataMixin
from odalc.mailer import send_odalc_email
from odalc.teachers.forms import CreateCourseForm, TeacherRegisterForm, TeacherEditForm
from odalc.teachers.models import TeacherUser


class TeacherRegisterView(UserDataMixin, CreateView):
    model = TeacherUser
    template_name = "teachers/teacher_register.html"
    form_class = TeacherRegisterForm
    success_url = reverse_lazy('teachers:dashboard')

    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def dispatch(self, request, *args, **kwargs):
        return super(TeacherRegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        a = super(TeacherRegisterView, self).form_valid(form)
        user = authenticate(username=self.request.POST['email'],
                         password=self.request.POST['password1'])
        login(self.request, user)
        return a


class TeacherEditView(UserDataMixin, UpdateView):
    model = TeacherUser
    template_name = "teachers/teacher_edit.html"
    form_class = TeacherEditForm
    success_url = reverse_lazy('teachers:dashboard')

    def get_object(self):
        return self.user

    def get_success_url(self):
        messages.success(self.request, 'Information updated')
        return super(TeacherEditView, self).get_success_url()

class CreateCourseView(UserDataMixin, FormView):
    model = Course
    template_name = 'teachers/create_course_form.html'
    form_class = CreateCourseForm
    success_url = reverse_lazy('teachers:dashboard')

    def form_valid(self, form):
        # Create a new Course Instance
        new_course = form.save(commit=False)
        new_course.teacher = self.request.user.child
        new_course.status = Course.STATUS_PENDING
        new_course.save()

        # Combine the separate date and time fields to create datetime instances
        start_datetime1 = dt.combine(form.cleaned_data.get('date1'), form.cleaned_data.get('start_time1'))
        start_datetime2 = dt.combine(form.cleaned_data.get('date2'), form.cleaned_data.get('start_time2'))
        start_datetime3 = dt.combine(form.cleaned_data.get('date3'), form.cleaned_data.get('start_time3'))
        end_datetime1 = dt.combine(form.cleaned_data.get('date1'), form.cleaned_data.get('end_time1'))
        end_datetime2 = dt.combine(form.cleaned_data.get('date2'), form.cleaned_data.get('end_time2'))
        end_datetime3 = dt.combine(form.cleaned_data.get('date3'), form.cleaned_data.get('end_time3'))

        # Create a CourseAvailability instance tied to the new Course
        new_course_availability = CourseAvailability(
            start_datetime1 = start_datetime1,
            start_datetime2 = start_datetime2,
            start_datetime3 = start_datetime3,
            end_datetime1 = end_datetime1,
            end_datetime2 = end_datetime2,
            end_datetime3 = end_datetime3,
            course = new_course
        )
        new_course_availability.save()

        # Notify admins and teachers about the course submission
        url_teacher_dashboard = 'http://' + self.request.get_host() + reverse('teachers:dashboard')
        url_admin_course_review = 'http://' + self.request.get_host() + reverse('admins:course_review', args=(new_course.id,))
        context = {
            'course': new_course,
            'url_teacher_dashboard': url_teacher_dashboard,
            'url_admin_course_review': url_admin_course_review,
        }
        send_odalc_email('notify_teacher_course_submitted', context, [new_course.teacher.email])
        send_odalc_email('notify_admins_course_submitted', context, [], cc_admins=True)
        messages.success(self.request, new_course.title + 'is now pending approval')
        return super(CreateCourseView, self).form_valid(form)


class TeacherDashboardView(UserDataMixin, TemplateView):
    template_name = "teachers/dashboard.html"

    def get_context_data(self, **kwargs):
        """
        Insert the single object into the context dict.
        """
        context = super(TeacherDashboardView, self).get_context_data(**kwargs)
        context['user'] = self.user
        user = TeacherUser.objects.get(id=self.user.id)
        courses = Course.objects.filter(teacher=user)
        context['pending_courses'] = courses.filter(status=Course.STATUS_PENDING).order_by('-start_datetime')
        context['active_courses'] = courses.filter(status=Course.STATUS_ACCEPTED).order_by('-start_datetime')
        context['finished_courses'] = courses.filter(status=Course.STATUS_FINISHED).order_by('-start_datetime')
        context['denied_courses'] = courses.filter(status=Course.STATUS_DENIED).order_by('-start_datetime')
        return context
