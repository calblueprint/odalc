from django.shortcuts import render
from django.views.generic import CreateView
from odalc.students.forms import FeedbackForm
from odalc.students.models import CourseFeedback
# Create your views here.

class SubmitCourseFeedback(CreateView):
	model = CourseFeedback
	template_name = 'students/course_feedback_form.html'
	form_class = FeedbackForm

