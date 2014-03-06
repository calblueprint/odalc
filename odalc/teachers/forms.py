from odalc.base.models import Course
from django.forms import ModelForm
from django import forms

class CreateCourseForm(ModelForm):

	start_datetime1 = forms.DateTimeField()
	end_datetime1 = forms.DateTimeField()

	start_datetime2 = forms.DateTimeField()
	end_datetime2 = forms.DateTimeField()

	start_datetime3 = forms.DateTimeField()
	end_datetime3 = forms.DateTimeField()

	class Meta:
		model = Course
		exclude = ['teacher', 'students', 'start_datetime', 'end_datetime']