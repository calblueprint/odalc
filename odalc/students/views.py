from django.core.urlresolvers import reverse_lazy, resolve
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib import messages

from odalc.base.views import UserDataMixin
from odalc.courses.models import Course, CourseFeedback
from odalc.students.forms import StudentRegisterForm, StudentEditForm, FeedbackForm
from odalc.students.models import StudentUser

class StudentRegisterView(UserDataMixin, CreateView):
    """Allows a student to register"""
    model = StudentUser
    template_name = "students/register.html"
    form_class = StudentRegisterForm
    success_url = reverse_lazy('home')

    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('home')
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
            print match
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

    def get_object(self):
        return self.user

    def get_success_url(self):
        messages.success(self.request, 'Information updated')
        return super(StudentEditView, self).get_success_url()


"""Controls course feedback submission for a particular student and course"""
class SubmitCourseFeedbackView(UserDataMixin, CreateView):
    model = CourseFeedback
    template_name = 'students/course_feedback_form.html'
    form_class = FeedbackForm

    def form_valid(self, form):
        course_feedback = form.save(commit=False)
        course_id = self.kwargs.get('pk', None)
        CourseFeedback.objects.create_from_form(form, course_id, self.user.id)
        messages.success(self.request, 'Feedback for submitted')
        return redirect('courses:detail', course_id)

    def get_context_data(self, **kwargs):
        context = super(SubmitCourseFeedbackView, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs.get('pk', None)
        context['title'] = Course.objects.get(pk=context['pk']).title
        return context

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated():
            return redirect('/accounts/login?next=%s' % self.request.path)
        course = Course.objects.get(pk=self.kwargs.get('pk', None))
        students = [student.email for student in course.students.all()]
        if ((user.has_perm('base.student_permission') and user.email in students) or
            user.has_perm('base.admin_permission')):
            return super(SubmitCourseFeedbackView, self).dispatch(*args, **kwargs)
        else:
            return self.deny_access()


class StudentDashboardView(UserDataMixin, TemplateView):
    """StudentDashboardView shows the student his/her basic information and
    courses taken."""
    template_name = "students/student_dashboard.html"

    def get_context_data(self, **kwargs):
        student_user = self.user
        context = super(StudentDashboardView, self).get_context_data(**kwargs)
        context['user'] = student_user
        context['courses_upcoming'] = Course.objects.get_all_active(student_user.course_set)
        context['courses_taken'] = Course.objects.get_finished(student_user.course_set)
        return context

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated():
            return redirect('/accounts/login?next=%s' % self.request.path)
        if user.has_perm('base.student_permission'):
            return super(StudentDashboardView, self).dispatch(*args, **kwargs)
        return self.deny_access()
