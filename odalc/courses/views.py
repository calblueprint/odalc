import datetime

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, UpdateView

from odalc.courses.forms import EditCourseForm
from odalc.courses.models import Course
from odalc.lib.payments import (
    MissingTokenException,
    handle_stripe_course_registration,
)
from odalc.users.views import UserDataMixin


class CourseDetailView(UserDataMixin, DetailView):
    """View for displaying a single Course object."""
    model = Course
    context_object_name = 'course'
    template_name = 'courses/course.html'

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            **response_kwargs
        )

    def dispatch(self, request, *args, **kwargs):
        self.set_perms(request, *args, **kwargs)
        course = self.get_object()
        # Redirect to the URL with the correct slug if the slug does not match
        if self.kwargs.get(self.slug_url_kwarg, None) != course.slug():
            return redirect(course, permanent=True)
        elif (
            course.is_accepted() or
            course.is_finished() or
            (self.user.is_authenticated() and (
                course.is_owner(self.user) or self.is_admin_user))
            ):
            return super(CourseDetailView, self).dispatch(request, *args, **kwargs)
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
        """On the template, the 'Enroll' button is disabled if the user is signed in as a teacher or admin. Only
        unauthenticated or users authenticated as students should be sending these POST requests.
        """
        course = self.get_object()
        if request.POST.get("login-redirect"):
            # Redirect them to the login page with this page as the 'next' URL if
            # a user wants to enroll but isn't signed in
            messages.info(request, "You must be signed in to enroll in a course.")
            response = redirect('users:login')
            response['Location'] += '?next=' + reverse('courses:detail', args=[course.pk, course.slug()])
            return response
        elif course.is_full():
            messages.error(request, "This course is already full. Your card hasn't been charged")
            return redirect(course)
        elif course.is_student_in_course(self.user):
            messages.error(request, "You are already signed up for this course. Your card hasn't been charged")
            return redirect(course)
        else:
            # User is signed in as a student and has clicked "enroll"
            try:
                token = request.POST.get('stripeToken', False)
                handle_stripe_course_registration(self.user, course, token)
                course.students.add(self.user)
                course.save()
                messages.success(request, "You have successfully registered for this course!")
                return redirect(course)
            except MissingTokenException:
                messages.error(request, "No payment information was included in your submission. Your card was not charged.")
                return redirect(course)
            except stripe.CardError:
                messages.error(request, "Your information was invalid or your card has been declined.")
                return self.render_to_response(self.get_context_data())


class CourseEditView(UserDataMixin, UpdateView):
    """View for editing course information. This is used by both teacher and admin users, but certain fields are set
    to read-only in the template depending on the user type.
    """

    model = Course
    form_class = EditCourseForm
    context_object_name = 'course'
    template_name = 'courses/course_edit.html'

    def dispatch(self, request, *args, **kwargs):
        self.set_perms(request, *args, **kwargs)
        course = self.get_object()
        if not self.user.is_authenticated():
            return redirect('/users/login?next=%s' % self.request.path)
        elif course.is_owner(self.user) or self.is_admin_user:
            return super(CourseEditView, self).dispatch(request, *args, **kwargs)
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


class CourseListingView(UserDataMixin, ListView):
    """View for displaying the courses offered. There are three categories of courses: all courses, past courses, and
    upcoming courses.
    """
    context_object_name = 'courses'
    paginate_by = 10
    template_name = 'courses/course_listing.html'

    PARAM_TYPE = "type"
    TYPE_UPCOMING = "upcoming"
    TYPE_PAST = "past"

    def dispatch(self, request, *args, **kwargs):
        self.set_perms(request, *args, **kwargs)
        return super(CourseListingView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = None
        courses_type = self.request.GET.get(CourseListingView.PARAM_TYPE)
        if courses_type == CourseListingView.TYPE_PAST:
            queryset =  Course.objects.get_finished()
        else:
            # Display courses coming up in the next year
            now = datetime.datetime.now()
            future = now + datetime.timedelta(days=365)
            queryset =  Course.objects.get_in_date_range(now, future)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CourseListingView, self).get_context_data(**kwargs)
        is_past = self.request.GET.get(CourseListingView.PARAM_TYPE) == CourseListingView.TYPE_PAST
        context['is_upcoming'] = not is_past
        context['is_past'] = is_past
        return context

