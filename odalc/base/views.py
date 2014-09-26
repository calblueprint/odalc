import datetime

from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import (
    DetailView,
    FormView,
    TemplateView,
    UpdateView,
    View
)

from odalc.base.forms import EditCourseForm
from odalc.courses.models import Course
from odalc.users.models import AdminUser, StudentUser, TeacherUser, User
from odalc.lib.payments import (
    MissingTokenException,
    handle_stripe_course_registration,
    handle_stripe_donation
)

import stripe


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


class CourseDetailView(UserDataMixin, DetailView):
    model = Course
    context_object_name = 'course'
    template_name = 'base/course.html'

    def dispatch(self, request, *args, **kwargs):
        handler = super(CourseDetailView, self).dispatch(request, *args, **kwargs)
        course = self.get_object()
        if (course.is_accepted() or course.is_finished() or
            (self.user.is_authenticated and (course.is_owner(self.user) or self.is_admin_user))):
            return handler
        else:
            return self.deny_access()

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        course = self.get_object()
        context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
        if self.user.is_authenticated():
            context['email'] = self.user.email
            context['in_class'] = course.is_student_in_course(self.user)
            context['submitted_feedback'] = course.is_student_feedback_submitted(self.user)
            context['is_past_start_date'] = course.is_past_start_date(datetime.datetime.now())
        context['cost_in_cents'] = course.get_cost_in_cents()
        context['course_full'] = course.is_full()
        context['course_finished'] = course.is_finished()
        context['open_seats'] = course.get_num_open_seats()
        context['is_owner'] = course.is_owner(self.user)
        return context

    def post(self, request, *args, **kwargs):
        course = self.get_object()
        if course.is_full():
            messages.error(request, "This course is already full. Your card hasn't been charged")
            return redirect('courses:detail', course.pk)
        if course.is_student_in_course(self.user):
            messages.error(request, "You are already signed up for this course. Your card hasn't been charged")
            return redirect('courses:detail', course.pk)
        try:
            token = request.POST.get('stripeToken', False)
            handle_stripe_course_registration(self.user, course, token)
            course.students.add(self.user)
            course.save()
            messages.success(request, "You have successfully registered for this course!")
            return redirect('courses:detail', course.pk)
        except MissingTokenException:
            messages.error(request, "No payment information was included in your submission. Your card was not charged.")
            return redirect('courses:detail', course.pk)
        except stripe.CardError:
            messages.error(request, "Your information was invalid or your card has been declined.")
            return self.render_to_response(self.get_context_data())


class CourseEditView(UserDataMixin, UpdateView):
    model = Course
    form_class = EditCourseForm
    context_object_name = 'course'
    template_name = 'base/course_edit.html'

    def dispatch(self, request, *args, **kwargs):
        handler = super(CourseEditView, self).dispatch(request, *args, **kwargs)
        course = self.get_object()
        if not self.user.is_authenticated():
            return redirect('/accounts/login?next=%s' % self.request.path)
        elif course.is_owner(self.user) or self.is_admin_user:
            return handler
        else:
            return self.deny_access()

    def get_context_data(self, **kwargs):
        context = super(CourseEditView, self).get_context_data(**kwargs)
        context['teacher_split'] = self.get_object().get_teacher_cost_split()
        return context

    def get_success_url(self):
        messages.success(self.request, self.get_object().title + ' edited successfully')
        if self.is_teacher_user:
            return reverse('teachers:dashboard')
        elif self.is_admin_user:
            return reverse('admins:dashboard')
        else:
            # Should never happen
            return reverse('home')


class CourseListingView(UserDataMixin, TemplateView):
    """Main view for displaying the courses offered. There are three categories of courses:
    all courses, past courses, and upcoming courses (courses coming up in the next month)"""
    template_name = 'base/course_listing.html'

    def get_context_data(self, **kwargs):
        context = super(CourseListingView, self).get_context_data(**kwargs)
        now = datetime.datetime.now()
        month_from_now = now + datetime.timedelta(days=30)
        context['all_courses'] = Course.objects.get_all_approved()
        context['past_courses'] = Course.objects.get_finished()
        context['upcoming_courses'] = Course.objects.get_in_date_range(now, month_from_now)
        return context


class HomePageView(UserDataMixin, TemplateView):
    """Landing page for the website. Also displays the next three upcoming
    courses as "featured courses". If there are not enough, it will display past
    courses as well."""
    NUM_COURSES_SHOWN = 3
    template_name = 'base/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['featured_courses'] = Course.objects.get_featured(
            HomePageView.NUM_COURSES_SHOWN)
        return context


class AboutPageView(UserDataMixin, TemplateView):
    template_name = 'base/about.html'


class DonatePageView(UserDataMixin, TemplateView):
    template_name = 'base/donate.html'

    def get_context_data(self, **kwargs):
        context = super(DonatePageView, self).get_context_data(**kwargs)
        context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
        return context

    def post(self, request, *args, **kwargs):
        # Get the credit card details submitted by the form
        token = request.POST.get('stripeToken', False)
        amount = request.POST.get('quantity', False)
        try:
            handle_stripe_donation(amount, token)
            messages.success(request, "Thank you! Your donation has been processed.")
            return redirect('donate')
        except MissingTokenException:
            messages.error(request, "No payment information was included in your submission. Your card hasn't been charged")
            return redirect('donate')
        except stripe.CardError:
            # The card has been declined
            messages.error(request, "Your information was invalid or your card has been declined")
            return self.render_to_response(self.get_context_data())


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

