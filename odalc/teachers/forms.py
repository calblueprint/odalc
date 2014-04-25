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
                  'organization',
                  'position',
                  'street_address',
                  'city',
                  'zipcode',
                  'phone',
                  'about',
                  'picture',
                  'resume',
                  'experience',
                  'info_source')

class TeacherEditForm(forms.ModelForm):
    class Meta:
        model = TeacherUser
        exclude = ('email', 'info_source')

class CreateCourseForm(forms.ModelForm):
    date1 = forms.DateField(label='First Choice for Date to Teach Course')
    start_time1 = forms.TimeField(label='Starting Time for Course Session')
    end_time1 = forms.TimeField(label='Ending Time for Course Session')

    date2 = forms.DateField(label='Second Choice for Date to Teach Course')
    start_time2 = forms.TimeField(label='Starting Time for Course Session')
    end_time2 = forms.TimeField(label='Ending Time for Course Session')

    date3 = forms.DateField(label='Third Choice for Date to Teach Course')
    start_time3 = forms.TimeField(label='Starting Time for Course Session')
    end_time3 = forms.TimeField(label='Ending Time for Course Session')

    class Meta:
        model = Course
        exclude = ['teacher', 'students', 'start_datetime', 'end_datetime', 'status']
