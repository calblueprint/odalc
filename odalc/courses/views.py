import datetime

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import DetailView, TemplateView, UpdateView

from odalc.courses.forms import EditCourseForm
from odalc.courses.models import Course
from odalc.lib.payments import (
    MissingTokenException,
    handle_stripe_course_registration,
)
from odalc.users.views import UserDataMixin


class CourseDetailView(UserDataMixin, DetailView):
    model = Course
    context_object_name = 'course'
    template_name = 'courses/course.html'

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
    template_name = 'courses/course_edit.html'

    def dispatch(self, request, *args, **kwargs):
        handler = super(CourseEditView, self).dispatch(request, *args, **kwargs)
        course = self.get_object()
        if not self.user.is_authenticated():
            return redirect('/users/login?next=%s' % self.request.path)
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
    template_name = 'courses/course_listing.html'

    def get_context_data(self, **kwargs):
        context = super(CourseListingView, self).get_context_data(**kwargs)
        now = datetime.datetime.now()
        month_from_now = now + datetime.timedelta(days=30)
        context['all_courses'] = Course.objects.get_all_approved()
        context['past_courses'] = Course.objects.get_finished()
        context['upcoming_courses'] = Course.objects.get_in_date_range(now, month_from_now)
        return context

