from django.shortcuts import render
from django.views.generic import CreateView
from odalc.base.models import Course

# Create your views here.
class CreateCourse(CreateView):
	model = Course
	template_name = 'teachers/create_course_form.html'

	def form_valid(self, form):
		if form.is_valid():
			
