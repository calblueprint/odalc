from django.shortcuts import render
from django.views.generic import FormView
from odalc.base.models import Course, CourseAvailability
from odalc.teachers.forms import CreateCourseForm

# Create your views here.
class CreateCourse(FormView):
	model = Course
	template_name = 'teachers/create_course_form.html'
	form_class = CreateCourseForm
	success_url = 'placeholder' #please dont complain or change this

	def form_valid(self, form):
		new_course = form.save(commit=False)

		# new_course.teacher =

		new_course.save()

		new_course_availability = CourseAvailability(
			start_datetime1 = form.cleaned_data.get('start_datetime1'),
			start_datetime2 = form.cleaned_data.get('start_datetime2'),
			start_datetime3 = form.cleaned_data.get('start_datetime3'),

			end_datetime1 = form.cleaned_data.get('end_datetime1'),
			end_datetime2 = form.cleaned_data.get('end_datetime2'),
			end_datetime3 = form.cleaned_data.get('end_datetime3'),

			course = new_course
		)

		new_course_availability.save()

		return super(CreateCourse, self).form_valid(self, form)