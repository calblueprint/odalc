from django.utils.translation import ugettext as _
from django import forms
from localflavor.us import forms as localflavor_forms
from odalc.teachers.models import TeacherUser

class TeacherCreateForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))
    phone = localflavor_forms.USPhoneNumberField(required=True, label='Phone')
    zipcode = localflavor_forms.USZipCodeField(required=True, label='Zipcode')

    class Meta:
        model = TeacherUser
        fields = ('email',
                  'street_address',
                  'city',
                  'zipcode',
                  'phone',
                  'about',
                  'picture',
                  'resume',
                  'experience',
                  'info_source')
