from django.shortcuts import render
from django.views.generic import CreateView
from odalc.students.forms import StudentRegisterForm
from odalc.students.models import StudentUser

# Create your views here.
class StudentRegisterView(CreateView):
	model = StudentUser
	template_name = "students/register.html"
	form_class = StudentRegisterForm