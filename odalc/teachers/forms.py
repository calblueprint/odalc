from django import forms
from localflavor.us import forms as localflavor_forms

from odalc.teachers.models import TeacherUser

class TeacherCreateForm(forms.ModelForm):
    phone = localflavor_forms.USPhoneNumberField()

    class Meta:
        model = TeacherUser
        exclude = ['phone', 'last_login']