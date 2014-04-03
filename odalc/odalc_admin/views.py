from django.views.generic import UpdateView
from odalc.base.models import Course
from odalc.mailer import send_odalc_emails
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy

# Create your views here.

class ApplicationReviewView(UpdateView):
    model = Course
    fields = [
        'title',
        'description',
        'size',
        'start_datetime',
        'end_datetime',
        'prereqs',
        'skill_level',
        'cost',
        'odalc_cost_split',
        'image',
        'additional_info',
    ]
    context_object_name = 'course'
    template_name = 'odalc_admin/course_application_review.html'
    success_url = reverse_lazy('home') #TODO

    def get_context_data(self, **kwargs):
        context = super(ApplicationReviewView, self).get_context_data(**kwargs)
        return context 

    def form_valid(self, form):
        course = self.object
        teacher = self.object.teacher
        context = {
            'course':course, 
            'teacher':teacher
        }
        
        if '_approve' in self.request.POST:
            #1. notify teacher of approval
            send_odalc_emails('approve',context,[teacher.email])
            #2. change status of course to "approved"
            course.status = course.STATUS_ACCEPTED
            course.save()
            #3. make course visible to all (permissions - John)
        elif '_deny' in self.request.POST:
            #1. notify teacher of denial 
            send_odalc_emails('deny',context,[teacher.email])
            #2. change status of course to "denied"
            course.status = course.STATUS_DENIED
            course.save()
        return redirect(ApplicationReviewView.success_url)

