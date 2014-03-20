from django.utils.translation import ugettext as _
from localflavor.us import forms as localflavor_forms
from odalc.base.forms import UserRegisterForm
from odalc.teachers.models import TeacherUser
from odalc.base.models import Course
from django import forms

class TeacherRegisterForm(UserRegisterForm):
    phone = localflavor_forms.USPhoneNumberField(required=True, label='Phone')
    zipcode = localflavor_forms.USZipCodeField(required=True, label='Zipcode')

    class Meta:
        model = TeacherUser
        fields = ('email',
                  'first_name',
                  'last_name',
                  'street_address',
                  'city',
                  'zipcode',
                  'phone',
                  'about',
                  'picture',
                  'resume',
                  'experience',
                  'info_source')

class CreateCourseForm(forms.ModelForm):

    start_datetime1 = forms.DateTimeField()
    end_datetime1 = forms.DateTimeField()

    start_datetime2 = forms.DateTimeField()
    end_datetime2 = forms.DateTimeField()

    start_datetime3 = forms.DateTimeField()
    end_datetime3 = forms.DateTimeField()

    class Meta:
        model = Course
        exclude = ['teacher', 'students', 'start_datetime', 'end_datetime']
