import re

from django import forms
from django.utils.safestring import mark_safe


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
                  'website',
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
                  'experience',
                  'website',
                  )


class CreateCourseForm(forms.ModelForm):
    date1 = forms.DateField(
        # I'm sorry I really am
        label=mark_safe('<strong>First Choice for Date</strong> to Teach Course')
    )
    start_time1 = forms.TimeField(
        label=mark_safe('<strong>Starting Time</strong> for Course Session')
    )
    end_time1 = forms.TimeField(
        label=mark_safe('<strong>Ending Time</strong> for Course Session')
    )

    date2 = forms.DateField(
        label=mark_safe('<strong>Second Choice</strong> for Date to Teach Course')
    )
    start_time2 = forms.TimeField(
        label=mark_safe('<strong>Starting Time</strong> for Course Session')
    )
    end_time2 = forms.TimeField(
        label=mark_safe('<strong>Ending Time</strong> for Course Session')
    )

    date3 = forms.DateField(
        label=mark_safe('<strong>Third Choice for Date</strong> to Teach Course')
    )
    start_time3 = forms.TimeField(
        label=mark_safe('<strong>Starting Time</strong> for Course Session')
    )
    end_time3 = forms.TimeField(
        label=mark_safe('<strong>Ending Time</strong> for Course Session')
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
            'image_thumbnail'
        )
