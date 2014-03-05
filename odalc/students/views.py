from django.shortcuts import render
from odalc.students.models import CourseFeedback
from django.views.generic import CreateView

# Create your views here.

class SubmitCourseFeedback(CreateView):
	model = CourseFeedback
	template_name = 'course_feedback_form.html'

	def get_success_url(self):
		return reverse('submit-success')