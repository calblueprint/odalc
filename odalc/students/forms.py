from django import forms
from odalc.students.models import StudentUser

class StudentRegisterForm(forms.ModelForm):

    class Meta:
        model = StudentUser
        exclude = ['last_login']