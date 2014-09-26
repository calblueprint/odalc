from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, View
from django.shortcuts import redirect

from odalc.users.models import User


class UserDataMixin(object):
    def deny_access(self):
        """Basic method to replace the default PermissionDenied()"""
        messages.error(
            self.request,
            'Oops! You do not have permission to access this page.'
        )
        return redirect('home')

    def dispatch(self, request, *args, **kwargs):
        """ dispatch() gets request.user and downcasts self.user to the actual
        user type, if possible. If the user isn't logged in, then self.user is
        an AnonymousUser, which is a built-in Django user type. If the user is
        logged in, self.user is either a TeacherUser, StudentUser, or
        AdminUser.
        """
        self.user = request.user
        if isinstance(self.user, User):
            self.user = self.user.child
            self.is_student_user = self.user.groups.filter(name="students").exists()
            self.is_teacher_user = self.user.groups.filter(name="teachers").exists()
            self.is_admin_user = self.user.groups.filter(name="odalc_admins").exists()
        else:
            self.is_student_user = False
            self.is_teacher_user = False
            self.is_admin_user = False
        return super(UserDataMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """ 'odalc_user' is included here for convenience. By default, the
        variable {{ user }} in the templates refers to 'request.user' above,
        which is either an AnonymousUser or a User (in odalc.base.models).
        We may want access to attributes in the downcasted user type, so to
        access these we can use {{ odalc_user }} in the templates.
        """
        context = super(UserDataMixin, self).get_context_data(**kwargs)
        context['odalc_user'] = self.user
        context['is_student_user'] = self.is_student_user
        context['is_teacher_user'] = self.is_teacher_user
        context['is_admin_user'] = self.is_admin_user
        return context


class LoginView(UserDataMixin, FormView):
    template_name = 'base/login.html'
    form_class = AuthenticationForm

    @method_decorator(sensitive_post_parameters('password'))
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('home')
        else:
            request.session.set_test_cookie()
            self.next_url = request.GET.get('next', 'home')
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        messages.error(self.request, 'Incorrect login or password. Note: Fields are case sensitive.')
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        messages.success(self.request, 'Logged in as ' + self.request.POST.get('username'))
        return redirect(self.next_url)


class LogoutView(UserDataMixin, View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        messages.success(self.request, 'Logged out successfully')
        return redirect('home')

