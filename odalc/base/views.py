from django.views.generic import DetailView, UpdateView, TemplateView, FormView, View
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.shortcuts import redirect
from django.contrib import messages
from odalc.base.models import Course
from odalc.teachers.forms import EditCourseForm
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied

# Create your views here.

class CourseDetailView(DetailView):
    model = Course
    context_object_name = 'course'
    template_name = 'base/course.html'

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        return context

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        course = self.get_object()
        if (course.status == Course.STATUS_ACCEPTED or
            (user.has_perm('base.teacher_permission') and course.teacher.email == user.email) or
            user.has_perm('base.admin_permission')):
            return super(CourseDetailView, self).dispatch(*args, **kwargs)
        raise PermissionDenied()

class CourseEditView(UpdateView):
    model = Course
    form_class = EditCourseForm
    context_object_name = 'course'
    template_name = 'base/course_edit.html'
    success_url = reverse_lazy('teachers:dashboard')

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        course = self.get_object()
        if ((user.has_perm('base.teacher_permission') and course.teacher.email == user.email) or
            user.has_perm('base.admin_permission')):
            return super(CourseEditView, self).dispatch(*args, **kwargs)
        raise PermissionDenied()

class HomePageView(TemplateView):
    template_name = 'base/home.html'

class LoginView(FormView):
    template_name = 'base/login.html'
    form_class = AuthenticationForm

    # TODO: Add proper redirection when urls/templates are better defined
    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        return redirect(self.next_url)

    def form_invalid(self, form):
        messages.error(self.request, 'Incorrect login or password')
        return self.render_to_response(self.get_context_data(form=form))

    @method_decorator(sensitive_post_parameters('password'))
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        self.next_url = request.GET.get('next', 'home')
        return super(LoginView, self).dispatch(request, *args, **kwargs)

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return redirect('home')
