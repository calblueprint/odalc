from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib import messages

from odalc.base.models import Course
from odalc.base.views import UserDataMixin
from odalc.students.forms import StudentRegisterForm, StudentEditForm, FeedbackForm
from odalc.students.models import CourseFeedback, StudentUser

"""Allows a student to register"""
class StudentRegisterView(UserDataMixin, CreateView):
    model = StudentUser
    template_name = "students/register.html"
    form_class = StudentRegisterForm
    success_url = reverse_lazy('home')

    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def dispatch(self, request, *args, **kwargs):
        return super(StudentRegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        resp = super(StudentRegisterView, self).form_valid(form)
        user = authenticate(
            username=self.request.POST['email'],
            password=self.request.POST['password1']
        )
        login(self.request, user)
        messages.success(self.request, 'Registration successful')
        return resp

"""Controls the editing of personal information by the student"""
class StudentEditView(UserDataMixin, UpdateView):
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
        pk = self.kwargs.get('pk', None)
        course_feedback.course = Course.objects.get(pk=pk)
        course_feedback.student = StudentUser.objects.get(id=self.user.id)
        course_feedback.save()
        messages.success(self.request, 'Feedback for submitted')
        return redirect('courses:detail', pk)

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
        return self.deny_access()

"""StudentDashboardView shows the student his/her basic information and courses taken."""
class StudentDashboardView(UserDataMixin, TemplateView):
    template_name = "students/student_dashboard.html"

    def get_context_data(self, **kwargs):
        student_user = self.user
        context = super(StudentDashboardView, self).get_context_data(**kwargs)
        context['user'] = student_user
        context["courses_taken"] = student_user.course_set.all().order_by('-start_datetime')
        return context

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated():
            return redirect('/accounts/login?next=%s' % self.request.path)
        if user.has_perm('base.student_permission'):
            return super(StudentDashboardView, self).dispatch(*args, **kwargs)
        return self.deny_access()