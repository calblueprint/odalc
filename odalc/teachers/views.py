from django.shortcuts import render
from django.views.generic import CreateView
from odalc.teachers.forms import TeacherCreateForm
from odalc.teachers.models import TeacherUser

# Create your views here.
class TeacherRegisteration(CreateView):
	model = TeacherUser
	template_name = "teachers/teacher_register.html"
	form_class = TeacherCreateForm