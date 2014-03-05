from django.shortcuts import render
from base.models import Course

# Create your views here.

class CreateCourse(CreateView):
	model = Course
	template_name = 'create_course_form.html'

	def get_success_url(self):
		return reverse('submit-success')