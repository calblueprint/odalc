import re

from django import forms

from odalc.courses.models import Course
from odalc.users.forms import UserRegisterForm
from odalc.users.models import TeacherUser

from localflavor.us import forms as localflavor_forms


class TeacherRegisterForm(UserRegisterForm):
    phone = localflavor_forms.USPhoneNumberField(required=True, label='Phone')
    zipcode = localflavor_forms.USZipCodeField(required=False, label='Zipcode')

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
                  'experience')


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

    def clean_prereqs(self):
        prereq_fields =  self.data.getlist('prereq_fields[]')
        if prereq_fields:
            return "\n".join(prereq_fields)
        else:
            return ""
        raise ValidationError(
            _('Invalid value: %(value)s'),
            code='invalid',
            params={'value': '42'},
        )

    class Meta:
        model = Course
        exclude = (
            'teacher',
            'students',
            'start_datetime',
            'end_datetime',
            'status',
            'is_featured'
        )
