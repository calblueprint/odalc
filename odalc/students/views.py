from django.shortcuts import render
from django.views.generic import CreateView
import forms
from models import CourseFeedback
# Create your views here.

class SubmitCourseFeedback(CreateView):
	model = CourseFeedback
	template_name = 'course_feedback_form.html'
	form_class = forms.FeedbackForm