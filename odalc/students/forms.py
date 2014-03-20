from django import forms
from odalc.base.forms import UserRegisterForm
from django.core.exceptions import ValidationError
from odalc.students.models import CourseFeedback, StudentUser

class StudentRegisterForm(UserRegisterForm):

    class Meta:
        model = StudentUser
        fields = ('email', 'first_name', 'last_name')

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = CourseFeedback
        exclude = ['course', 'student']
