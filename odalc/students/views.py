from django.core.urlresolvers import reverse_lazy, resolve
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib import messages

from odalc.courses.models import Course, CourseFeedback
from odalc.students.forms import StudentRegisterForm, StudentEditForm, FeedbackForm
from odalc.users.models import StudentUser
from odalc.users.views import UserDataMixin

class StudentRegisterView(UserDataMixin, CreateView):
    """Allows a student to register"""
    model = StudentUser
    template_name = "students/register.html"
    form_class = StudentRegisterForm
    success_url = reverse_lazy('home')

    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def dispatch(self, request, *args, **kwargs):
        self.set_perms(request, *args, **kwargs)
        if request.user.is_authenticated():
            return redirect('home')
        else:
            return super(StudentRegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        super(StudentRegisterView, self).form_valid(form)
        user = authenticate(
            username=self.request.POST['email'],
            password=self.request.POST['password1']
        )
        login(self.request, user)
        messages.success(self.request, 'Account created successfully')
        self.next_url = self.request.POST.get('next', None)
        if self.next_url:
            match = resolve(self.next_url)
            if match.namespace == 'courses' and match.url_name == 'detail':
                messages.info(
                    self.request,
                    'You have created an account, but you are not yet enrolled in the course. Please click "Enroll" again to register for the course.'
                )
            return redirect(self.next_url)
        else:
            return redirect(StudentRegisterView.success_url)


class StudentEditView(UserDataMixin, UpdateView):
    """Controls the editing of personal information by the student"""
    model = StudentUser
    template_name = "students/student_edit.html"
    form_class = StudentEditForm
    success_url = reverse_lazy('students:dashboard')

    def dispatch(self, request, *args, **kwargs):
        self.set_perms(request, *args, **kwargs)
        return super(StudentEditView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        return self.user

    def get_success_url(self):
        messages.success(self.request, 'Information updated')
        return super(StudentEditView, self).get_success_url()


class SubmitCourseFeedbackView(UserDataMixin, CreateView):
    """Controls course feedback submission for a particular student and course"""
    model = CourseFeedback
    template_name = 'students/course_feedback_form.html'
    form_class = FeedbackForm

    def dispatch(self, request, *args, **kwargs):
        self.set_perms(request, *args, **kwargs)
        # The course is guaranteed to exist!
        self.course = Course.objects.get(pk=kwargs.get('pk', None))
        if not self.user.is_authenticated():
            return redirect('/users/login?next=%s' % self.request.path)
        if self.is_student_user and self.course.is_student_in_course(self.user):
            return super(SubmitCourseFeedbackView, self).dispatch(request, *args, **kwargs)
        else:
            return self.deny_access()

    def form_valid(self, form):
        CourseFeedback.objects.create_from_form(form, self.course.id, self.user.id)
        messages.success(self.request, 'Feedback for submitted')
        return redirect(self.course)

    def get_context_data(self, **kwargs):
        context = super(SubmitCourseFeedbackView, self).get_context_data(**kwargs)
        context['course'] = self.course
        return context


class StudentDashboardView(UserDataMixin, TemplateView):
    """StudentDashboardView shows the student his/her basic information and
    courses taken."""
    template_name = "students/student_dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        self.set_perms(request, *args, **kwargs)
        if not self.user.is_authenticated():
            return redirect('/users/login?next=%s' % self.request.path)
        elif self.is_student_user:
            return super(StudentDashboardView, self).dispatch(request, *args, **kwargs)
        else:
            return self.deny_access()

    def get_context_data(self, **kwargs):
        context = super(StudentDashboardView, self).get_context_data(**kwargs)
        context['user'] = self.user
        context['courses_upcoming'] = Course.objects.get_all_active(self.user.course_set)
        context['courses_taken'] = Course.objects.get_finished(self.user.course_set)
        return context
