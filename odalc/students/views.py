from django.shortcuts import render, redirect
from django.views.generic import CreateView
from odalc.students.forms import FeedbackForm
from odalc.students.models import CourseFeedback
from django.core.urlresolvers import reverse_lazy

# Create your views here.

class SubmitCourseFeedbackView(CreateView):
	model = CourseFeedback
	template_name = 'students/course_feedback_form.html'
	form_class = FeedbackForm
	success_url = reverse_lazy('home')

	def form_valid(self, form):
		course_feedback = form.save(commit=False)
		pk = self.kwargs.get('pk', None)
		course_feedback.course = Course.objects.get(pk=pk)
		course_feedback.student = Students.objects.order_by('?').first()
		course_feedback.save()
		return redirect(self.get_success_url())


	def get_context_data(self, **kwargs):
		context = super(SubmitCourseFeedbackView, self).get_context_data(**kwargs)
		context['pk'] = self.kwargs.get('pk', None)
		return context