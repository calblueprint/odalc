from django.shortcuts import redirect
from django.views.generic import CreateView
from odalc.students.forms import StudentRegisterForm, FeedbackForm
from odalc.students.models import CourseFeedback, StudentUser
from odalc.base.models import Course
from django.core.urlresolvers import reverse_lazy

# Create your views here.
class StudentRegisterView(CreateView):
    model = StudentUser
    template_name = "students/register.html"
    form_class = StudentRegisterForm
    success_url = reverse_lazy('home')


class SubmitCourseFeedbackView(CreateView):
    model = CourseFeedback
    template_name = 'students/course_feedback_form.html'
    form_class = FeedbackForm

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        # TODO: Error checking to make sure that user is a StudentUser
        return super(SubmitCourseFeedbackView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        course_feedback = form.save(commit=False)
        pk = self.kwargs.get('pk', None)
        course_feedback.course = Course.objects.get(pk=pk)
        course_feedback.student = StudentUser.objects.get(id=self.user.id)
        course_feedback.save()
        return redirect('courses:detail', pk)

    def get_context_data(self, **kwargs):
        context = super(SubmitCourseFeedbackView, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs.get('pk', None)
        return context
