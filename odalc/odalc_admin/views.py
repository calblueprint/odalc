from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Avg
from django.shortcuts import redirect
from django.views.generic import UpdateView,TemplateView,DetailView

from odalc.base.forms import EditCourseForm
from odalc.base.models import Course
from odalc.base.views import UserDataMixin
from odalc.mailer import send_odalc_email
from odalc.students.models import StudentUser
from odalc.teachers.models import TeacherUser


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

    def get_context_data(self, **kwargs):
        context = super(ApplicationReviewView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        course = self.object
        teacher = self.object.teacher
        context = {
            'course': course,
            'course_url': 'http://' + self.request.get_host() + reverse('courses:detail', args=(course.id,))
        }
        if '_approve' in self.request.POST:
            #1. change status of course to "approved"
            course.status = course.STATUS_ACCEPTED
            course.save()
            #2. notify teacher of approval
            send_odalc_email('notify_teacher_course_approved', context, [teacher.email], cc_admins=True)
            #3. make course visible to all (permissions - John)
        elif '_deny' in self.request.POST:
            #1. change status of course to "denied"
            course.status = course.STATUS_DENIED
            course.save()
            #2. notify teacher of denial
            send_odalc_email('notify_teacher_course_denied', context, [teacher.email], cc_admins=True)
        return redirect(ApplicationReviewView.success_url)

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated():
            return redirect('/accounts/login?next=%s' % self.request.path)
        if user.has_perm('base.admin_permission'):
            return super(ApplicationReviewView, self).dispatch(*args, **kwargs)
        raise PermissionDenied()


#TODO: show some teacher and student info as well
class AdminDashboardView(UserDataMixin, TemplateView):
    """AdminDashboardView shows the admin all pending course applications, current (live) courses,
    as well as finished courses and links to feedback for those finished courses
    """
    template_name = 'odalc_admin/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(AdminDashboardView, self).get_context_data(**kwargs)
        context['pending_courses'] = Course.objects.filter(status=Course.STATUS_PENDING)
        context['live_courses'] = Course.objects.filter(status=Course.STATUS_ACCEPTED)
        context['finished_courses'] = Course.objects.filter(status=Course.STATUS_FINISHED)
        context['teachers'] = TeacherUser.objects.all()
        context['students'] = StudentUser.objects.all()
        return context

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated():
            return redirect('/accounts/login?next=%s' % self.request.path)
        if user.has_perm('base.admin_permission'):
            return super(AdminDashboardView, self).dispatch(*args, **kwargs)
        raise PermissionDenied()


class CourseFeedbackView(UserDataMixin, DetailView):
    """CourseFeedbackView shows all the student feedback responses for a particular course,
    as well as aggregate data (averages) for the feedback
    """
    template_name = 'odalc_admin/course_feedback.html'
    model = Course

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        self.object = self.get_object()
        if not user.is_authenticated():
            return redirect('/accounts/login?next=%s' % self.request.path)
        if (user.has_perm('base.admin_permission') or (user.has_perm('base.teacher_permission') and self.object.teacher.id==user.id)):
            return super(CourseFeedbackView, self).dispatch(*args, **kwargs)
        raise PermissionDenied()


    def get_context_data(self, **kwargs):
        course = self.object
        forms = course.coursefeedback_set.all()
        context = super(CourseFeedbackView, self).get_context_data(**kwargs)
        context['feedback_forms'] = forms
        context['num_forms'] = course.coursefeedback_set.count()
        context['q1_avg'] = forms.aggregate(Avg('knowledgeable_of_subject'))['knowledgeable_of_subject__avg']
        context['q2_avg'] = forms.aggregate(Avg('encourages_questions'))['encourages_questions__avg']
        context['q3_avg'] = forms.aggregate(Avg('teaching_effectiveness'))['teaching_effectiveness__avg']
        context['q4_avg'] = forms.aggregate(Avg('applicable_to_needs'))['applicable_to_needs__avg']
        context['q5_avg'] = forms.aggregate(Avg('would_recommend'))['would_recommend__avg']
        context['q6_avg'] = forms.aggregate(Avg('course_inspiring'))['course_inspiring__avg']

        visualization = []
        for i in range(6):
            visualization.append([])
        scores = forms.values_list(
            'knowledgeable_of_subject',
            'encourages_questions',
            'teaching_effectiveness',
            'applicable_to_needs',
            'would_recommend',
            'course_inspiring'
            )
        for student in scores:
            for index, score in enumerate(student):
                visualization[index].append(score)
        context['visualization'] = visualization 

        return context
