import time, json, base64, hmac, urllib
from hashlib import sha1

from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import DetailView, UpdateView, TemplateView, FormView, View

from odalc.base.forms import EditCourseForm
from odalc.base.models import Course, User
from odalc.odalc_admin.models import AdminUser
from odalc.students.models import StudentUser
from odalc.teachers.models import TeacherUser

import stripe


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
        course = self.object
        context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
        if self.user.is_authenticated():
            context['email'] = self.user.email
            context['in_class'] = course.students.filter(id=self.user.id).exists()
        context['cost_in_cents'] = int(course.cost * 100)
        context['course_full'] = course.students.count() >= course.size
        context['open_seats'] = course.size - course.students.count()
        context['is_owner'] = (self.user.has_perm('base.teacher_permission') and course.teacher.email == self.user.email)
        return context

    def dispatch(self, request, *args, **kwargs):
        self.user = self.request.user
        course = self.get_object()
        if (course.status == Course.STATUS_ACCEPTED or
            (self.user.has_perm('base.teacher_permission') and course.teacher.email == self.user.email) or
            self.user.has_perm('base.admin_permission')):
            return super(CourseDetailView, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        course = self.object
        context = self.get_context_data(object=course)

        # Set your secret key: remember to change this to your live secret key in production
        # See your keys here https://manage.stripe.com/account
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Get the credit card details submitted by the form
        token = request.POST.get('stripeToken', False)
        if not token:
            messages.error(request, "No payment information was included in your submission. Your card hasn't been charged")
            return redirect('courses:detail',course.pk)

        # Create the charge on Stripe's servers - this will charge the user's card
        if context['course_full']:
            messages.error(request, "This course is already full. Your card hasn't been charged")
            return redirect('courses:detail',course.pk)
        if context['in_class']:
            messages.error(request, "You are already signed up for this course. Your card hasn't been charged")
            return redirect('courses:detail',course.pk)
        try:
          charge = stripe.Charge.create(
              amount=int(course.cost * 100), # amount in cents, again
              currency="usd",
              card=token,
              description='This is a payment for ' + self.object.title,
              metadata={
                'first_name':self.user.first_name,
                'last_name':self.user.last_name,
                'email':self.user.email,
                'course':course.title,
                'teacher_first_name':course.teacher.first_name,
                'teacher_last_name':course.teacher.last_name,
                'teacher_email':course.teacher.email,
                'odalc_funds': course.odalc_cost_split
                }
          )
        except stripe.CardError, e:
          # The card has been declined
            return self.render_to_response(self.get_context_data())

        #add student to course
        course.students.add(self.user)
        course.save()
        return redirect('courses:detail',course.pk)


class CourseEditView(UserDataMixin, UpdateView):
    model = Course
    form_class = EditCourseForm
    context_object_name = 'course'
    template_name = 'base/course_edit.html'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated():
            return redirect('/accounts/login?next=%s' % self.request.path)
        course = self.get_object()
        if ((user.has_perm('base.teacher_permission') and course.teacher.email == user.email) or
            user.has_perm('base.admin_permission')):
            return super(CourseEditView, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied()

    def get_success_url(self):
        if self.is_teacher_user:
            return reverse('teachers:dashboard')
        elif self.is_admin_user:
            return reverse('admins:dashboard')
        else:
            # Should never happen
            return reverse('home')


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
        if request.user.is_authenticated():
            return redirect('home')
        request.session.set_test_cookie()
        self.next_url = request.GET.get('next', 'home')
        return super(LoginView, self).dispatch(request, *args, **kwargs)


class LogoutView(UserDataMixin, View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return redirect('home')


class SignS3View(View):
    def get(self, request, *args, **kwargs):
        # Load necessary information into the application:
        AWS_ACCESS_KEY = settings.AWS_ACCESS_KEY_ID.strip()
        AWS_SECRET_KEY = settings.AWS_SECRET_ACCESS_KEY.strip()
        S3_BUCKET = settings.S3_BUCKET.strip()

        # Collect information on the file from the GET parameters of the request:
        object_name = urllib.quote_plus(request.GET.get('s3_object_name'))
        mime_type = request.GET.get('s3_object_type')

        # Set the expiry time of the signature (in seconds) and declare the permissions of the file to be uploaded
        expires = int(time.time()+10)
        amz_headers = "x-amz-acl:public-read"

        # Generate the PUT request that JavaScript will use:
        put_request = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, S3_BUCKET, object_name)

        # Generate the signature with which the request can be signed:
        signature = base64.encodestring(hmac.new(AWS_SECRET_KEY, put_request, sha1).digest())
        # Remove surrounding whitespace and quote special characters:
        signature = urllib.quote_plus(signature.strip())

        # Build the URL of the file in anticipation of its imminent upload:
        url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, object_name)

        get_params = urllib.urlencode({
            'AWSAccessKeyId': AWS_ACCESS_KEY,
            'Expires': expires,
            'Signature': signature
        })
        content = json.dumps({
            'signed_request': '%s?%s' % (url, get_params),
            'url': url
        })

        # Return the signed request and the anticipated URL back to the browser in JSON format:
        return HttpResponse(content, content_type='text/plain; charset=x-user-defined')
