from datetime import datetime as dt

from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    View,
)
from django.contrib import messages

from odalc.courses.forms import EditCourseForm
from odalc.courses.models import Course
from odalc.lib.mailer import send_odalc_email
from odalc.odalc_admin.forms import AdminEditForm, AdminRegisterForm
from odalc.users.models import AdminUser, StudentUser, TeacherUser
from odalc.users.views import UserDataMixin


class ApplicationReviewView(UserDataMixin, UpdateView):
    """A teacher must submit an application if he/she wants to teach a course, which will be
    reviewed by an admin. This application includes the proposed name, size, length, prereqs,
    cost, etc of the course. This ApplicationReviewView shows the admin that application and
    allows the admin to make final adjustments to these fields.
    """
    model = Course
    form_class = EditCourseForm
    context_object_name = 'course'
    template_name = 'odalc_admin/course_application_review.html'
    success_url = reverse_lazy('admins:dashboard')

    def dispatch(self, request, *args, **kwargs):
        self.set_perms(request, *args, **kwargs)
        if not self.user.is_authenticated():
            return redirect('/users/login?next=%s' % self.request.path)
        elif self.is_admin_user:
            return super(ApplicationReviewView, self).dispatch(request, *args, **kwargs)
        else:
            return self.deny_access()

    def form_valid(self, form):
        course = form.save(commit=False)
        teacher = course.teacher
        context = {}
        context['course'] = course
        context['course_url'] = 'https://' + self.request.get_host() + reverse('courses:detail', args=(course.id, course.slug()))
        context['facebook_share'] = 'http://www.facebook.com/sharer.php?u=' + context['course_url']
        context['twitter_share'] = 'https://twitter.com/home?status=Check%20out%20this%20new%20course%20that%20just%20went%20live%20at%20Oakland%20Digital!%20'+ context['course_url'] + '%20%23OaklandDigital%20via%20@ODALC'
        context['google_share'] = 'https://plus.google.com/share?url=' + context['course_url']


        if '_approve' in self.request.POST:
            start_time = form.cleaned_data.get('start_time')
            end_time = form.cleaned_data.get('end_time')
            date = form.cleaned_data.get('date')

            #1. Check to see if they added times and dates
            if not start_time or not end_time or not date:
                messages.error(self.request, 'Please choose a date start time and end time before approval')
                return redirect('/admins/review/%s' % course.id)

            #2. change status of course to "approved"
            Course.objects.approve_course(course, date, start_time, end_time)

            #3. notify teacher of approval
            send_odalc_email('notify_teacher_course_approved', context, [teacher.email], cc_admins=True)

            messages.success(self.request, course.title + ' has been approved')
        elif '_deny' in self.request.POST:
            #1. change status of course to "denied"
            Course.objects.deny_course(course)

            #2. notify teacher of denial
            send_odalc_email('notify_teacher_course_denied', context, [teacher.email], cc_admins=True)

            messages.error(self.request, course.title + ' has been denied')
        elif '_save' in self.request.POST:
            start_time = form.cleaned_data.get('start_time')
            end_time = form.cleaned_data.get('end_time')
            date = form.cleaned_data.get('date')

            #1. Check to see if they added times and dates
            if start_time and end_time and date:
                course.set_datetimes(date, start_time, end_time)

            messages.info(self.request, 'Changes to ' + course.title + ' have been saved.')
        course.save()
        return redirect(ApplicationReviewView.success_url)


class AdminDashboardView(UserDataMixin, ListView):
    """AdminDashboardView shows the admin all pending course applications, current (live) courses,
    as well as finished courses and links to feedback for those finished courses
    """
    context_object_name = 'courses'
    paginate_by = 10
    template_name = 'odalc_admin/admin_dashboard.html'

    PARAM_TYPE = "type"
    TYPE_PENDING = "pending"
    TYPE_ACTIVE = "active"
    TYPE_FINISHED = "finished"
    TYPE_DENIED = "denied"


    def dispatch(self, request, *args, **kwargs):
        self.set_perms(request, *args, **kwargs)
        self.is_active = (self.request.GET.get(AdminDashboardView.PARAM_TYPE)
                            == AdminDashboardView.TYPE_ACTIVE)
        self.is_finished = (self.request.GET.get(AdminDashboardView.PARAM_TYPE)
                            == AdminDashboardView.TYPE_FINISHED)
        self.is_denied = (self.request.GET.get(AdminDashboardView.PARAM_TYPE)
                            == AdminDashboardView.TYPE_DENIED)
        self.is_pending = ((self.request.GET.get(AdminDashboardView.PARAM_TYPE)
                            == AdminDashboardView.TYPE_PENDING) or (
                            not self.is_active and not self.is_finished and not self.is_denied))
        if not self.user.is_authenticated():
            return redirect('/users/login?next=%s' % self.request.path)
        elif self.is_admin_user:
            return super(AdminDashboardView, self).dispatch(request, *args, **kwargs)
        else:
            return self.deny_access()

    def get_queryset(self):
        queryset = None
        if self.is_active:
           queryset = Course.objects.get_all_active()
        elif self.is_finished:
           queryset = Course.objects.get_finished()
        elif self.is_denied:
           queryset = Course.objects.get_denied()
        else:
            # The default is pending courses
           queryset = Course.objects.get_pending()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AdminDashboardView, self).get_context_data(**kwargs)
        context['is_pending'] = self.is_pending
        context['is_active'] = self.is_active
        context['is_finished'] = self.is_finished
        context['is_denied'] = self.is_denied
        if self.is_pending:
            context['title'] = 'Courses Pending Review'
        if self.is_active:
            context['title'] = 'Active Courses'
        if self.is_finished:
            context['title'] = 'Finished Courses'
        if self.is_denied:
            context['title'] = 'Denied Courses'
        return context


class AJAXAdminDashboardView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(AJAXAdminDashboardView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        Course.objects.toggle_featured(
            request.POST.get('courseId'),
            request.POST.get('isFeatured') == 'true'
        )
        return HttpResponse('')


class CourseFeedbackView(UserDataMixin, DetailView):
    """CourseFeedbackView shows all the student feedback responses for a particular course,
    as well as aggregate data (averages) for the feedback
    """
    template_name = 'odalc_admin/course_feedback.html'
    model = Course

    def dispatch(self, request, *args, **kwargs):
        self.set_perms(request, *args, **kwargs)
        course = self.get_object()
        if not self.user.is_authenticated():
            return redirect('/users/login?next=%s' % self.request.path)
        elif self.is_admin_user or course.is_owner(self.user):
            return super(CourseFeedbackView, self).dispatch(request, *args, **kwargs)
        else:
            return self.deny_access()

    def get_context_data(self, **kwargs):
        course = self.object
        forms = course.coursefeedback_set.all()
        context = super(CourseFeedbackView, self).get_context_data(**kwargs)
        context['feedback_forms'] = forms
        questions = [
            'knowledgeable_of_subject',
            'encourages_questions',
            'teaching_effectiveness',
            'applicable_to_needs',
            'would_recommend',
            'course_inspiring'
        ]
        context['num_forms'] = course.coursefeedback_set.count()
        context['avg_list'] = []
        for index, question in enumerate(questions):
            context['q'+ str(index + 1) +'_avg'] = forms.aggregate(Avg(question))[question + '__avg']
            context['avg_list'].append(context['q'+ str(index + 1) +'_avg'])
        context['visualization'] = []
        scores = forms.values_list(*questions)
        for index, item in enumerate(scores):
            context['visualization'].append(list(item))
        return context


class AdminEditView(UserDataMixin, UpdateView):
    model = AdminUser
    template_name = "odalc_admin/admin_edit.html"
    form_class = AdminEditForm
    success_url = reverse_lazy('admins:dashboard')

    def dispatch(self, request, *args, **kwargs):
        self.set_perms(request, *args, **kwargs)
        return super(AdminEditView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        return self.user

    def get_success_url(self):
        messages.success(self.request, 'Information updated')
        return super(AdminEditView, self).get_success_url()


class AdminRegisterView(UserDataMixin, CreateView):
    model = AdminUser
    template_name = "odalc_admin/register.html"
    form_class = AdminRegisterForm
    success_url = reverse_lazy('admins:dashboard')

    def dispatch(self, request, *args, **kwargs):
        self.set_perms(request, *args, **kwargs)
        if not self.user.is_authenticated():
            return redirect('/users/login?next=%s' % self.request.path)
        elif self.is_admin_user:
            return super(AdminRegisterView, self).dispatch(request, *args, **kwargs)
        else:
            return self.deny_access()

    def form_valid(self, form):
        admin_name = form.cleaned_data.get('first_name') + ' ' + form.cleaned_data.get('last_name')
        context = {
            'admin_name': admin_name
        }
        send_odalc_email('notify_admins_new_admin', context, [], cc_admins=True)
        return super(AdminRegisterView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'New admin created')
        return super(AdminRegisterView, self).get_success_url()
