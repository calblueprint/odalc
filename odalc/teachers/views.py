from django.shortcuts import render
from odalc.base.models import Course

# Create your views here.
class CreateCourse(CreateView):
	model = Course
	template_name = 'teachers/create_course_form.html'