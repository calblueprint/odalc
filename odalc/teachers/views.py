from django.contrib.auth import login, authenticate
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView

from odalc.base.models import Course, CourseAvailability
from odalc.base.views import UserDataMixin
from odalc.mailer import send_odalc_email
from odalc.teachers.forms import CreateCourseForm, TeacherRegisterForm
from odalc.teachers.models import TeacherUser

# Create your views here.
class TeacherRegisteration(UserDataMixin, CreateView):
    model = TeacherUser
    template_name = "teachers/teacher_register.html"
    form_class = TeacherRegisterForm
    success_url = reverse_lazy('teachers:dashboard')

    def form_valid(self, form):
        a = super(TeacherRegisteration, self).form_valid(form)
        user = authenticate(username=self.request.POST['email'],
                         password=self.request.POST['password1'])
        login(self.request, user)
        return a


class CreateCourse(UserDataMixin, FormView):
    model = Course
    template_name = 'teachers/create_course_form.html'
    form_class = CreateCourseForm
    success_url = reverse_lazy('teachers:dashboard')

    def form_valid(self, form):
        new_course = form.save(commit=False)

        new_course.teacher = self.request.user.child
        new_course.status = Course.STATUS_PENDING

        new_course.save()

        new_course_availability = CourseAvailability(
            start_datetime1 = form.cleaned_data.get('start_datetime1'),
            start_datetime2 = form.cleaned_data.get('start_datetime2'),
            start_datetime3 = form.cleaned_data.get('start_datetime3'),

            end_datetime1 = form.cleaned_data.get('end_datetime1'),
            end_datetime2 = form.cleaned_data.get('end_datetime2'),
            end_datetime3 = form.cleaned_data.get('end_datetime3'),

            course = new_course
        )

        new_course_availability.save()
        url_teacher_dashboard = 'http://' + self.request.get_host() + reverse('teachers:dashboard')
        url_admin_course_review = 'http://' + self.request.get_host() + reverse('admins:course_review', args=(new_course.id,))
        context = {
            'course': new_course,
            'url_teacher_dashboard': url_teacher_dashboard,
            'url_admin_course_review': url_admin_course_review,
        }
        send_odalc_email('notify_teacher_course_submitted', context, [new_course.teacher.email])
        send_odalc_email('notify_admins_course_submitted', context, [], cc_admins=True)
        return super(CreateCourse, self).form_valid(form)

class TeacherDashboardView(UserDataMixin, TemplateView):
    template_name = "teachers/dashboard.html"

    def get_context_data(self, **kwargs):
        """
        Insert the single object into the context dict.
        """
        context = super(TeacherDashboardView, self).get_context_data(**kwargs)
        context['user'] = self.user
        user = TeacherUser.objects.get(id=self.user.id)
        context['courses'] = Course.objects.filter(teacher=user)
        return context
