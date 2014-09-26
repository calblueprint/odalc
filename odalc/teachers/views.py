from datetime import datetime as dt

from django.contrib.auth import login, authenticate
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import CreateView, FormView, TemplateView, UpdateView
from django.contrib import messages

from odalc.courses.models import Course, CourseAvailability
from odalc.base.views import UserDataMixin
from odalc.lib.mailer import send_odalc_email
from odalc.teachers.forms import CreateCourseForm, TeacherRegisterForm, TeacherEditForm
from odalc.users.models import TeacherUser


class TeacherRegisterView(UserDataMixin, CreateView):
    model = TeacherUser
    template_name = "teachers/teacher_register.html"
    form_class = TeacherRegisterForm
    success_url = reverse_lazy('teachers:dashboard')

    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('home')
        return super(TeacherRegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(
            username=self.request.POST['email'],
            password=self.request.POST['password1']
        )
        login(self.request, user)
        return super(TeacherRegisterView, self).form_valid(form)


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
        new_course = Course.objects.create_from_form(form, self.request.user.child)

        # Create a CourseAvailability instance tied to the new Course
        CourseAvailability.objects.create_from_form_data(form.cleaned_data, new_course)

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
        context = super(TeacherDashboardView, self).get_context_data(**kwargs)
        owned_courses = Course.objects.filter(teacher=self.user)
        context['user'] = self.user
        context['pending_courses'] = Course.objects.get_pending(owned_courses)
        context['active_courses'] = Course.objects.get_all_active(owned_courses)
        context['finished_courses'] = Course.objects.get_finished(owned_courses)
        context['denied_courses'] = Course.objects.get_denied(owned_courses)
        return context
