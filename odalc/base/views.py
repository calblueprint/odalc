from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import DetailView, UpdateView, TemplateView, FormView, View

from odalc.base.models import Course, User
from odalc.odalc_admin.models import AdminUser
from odalc.students.models import StudentUser
from odalc.teachers.models import TeacherUser
from odalc.teachers.forms import EditCourseForm

from django.core.urlresolvers import reverse_lazy
import stripe, json
from django.conf import settings

# Create your views here.

class UserDataMixin(object):
    def dispatch(self, request, *args, **kwargs):
        """ dispatch() gets request.user and downcasts self.user to the actual
        user type, if possible. If the user isn't logged in, then self.user is
        an AnonymousUser, which is a built-in Django user type. If the user is
        logged in, self.user is either a TeacherUser, StudentUser, or
        AdminUser.
        """
        self.user = request.user
        if isinstance(self.user, User):
            self.is_student_user = isinstance(self.user.child, StudentUser)
            self.is_teacher_user = isinstance(self.user.child, TeacherUser)
            self.is_admin_user = isinstance(self.user.child, AdminUser)
            self.user = self.user.child
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


class CourseDetailView(UserDataMixin, DetailView):
    model = Course
    context_object_name = 'course'
    template_name = 'base/course.html'

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
        context['email'] = self.user.email
        return context

    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        self.user = request.user
        return super(CourseDetailView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        # Set your secret key: remember to change this to your live secret key in production
        # See your keys here https://manage.stripe.com/account
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Get the credit card details submitted by the form
        token = request.POST['stripeToken']
        stripe_json = json.loads(request.POST['json'])
        print stripe_json

        # Create the charge on Stripe's servers - this will charge the user's card
        try:
          charge = stripe.Charge.create(
              amount=1000, # amount in cents, again
              currency="usd",
              card=token,
              description="payinguser@example.com"
          )
        except stripe.CardError, e:
          # The card has been declined
          pass


        return super(BaseCreateView, self).post(request, *args, **kwargs)

class CourseEditView(UserDataMixin, UpdateView):
    model = Course
    form_class = EditCourseForm
    context_object_name = 'course'
    template_name = 'base/course_edit.html'
    success_url = reverse_lazy('teachers:dashboard')


class HomePageView(UserDataMixin, TemplateView):
    template_name = 'base/home.html'


class AboutPageView(UserDataMixin, TemplateView):
    template_name = 'base/about.html'


class DonatePageView(UserDataMixin, TemplateView):
    template_name = 'base/donate.html'


class LoginView(UserDataMixin, FormView):
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

class LogoutView(UserDataMixin, View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return redirect('home')
