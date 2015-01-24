from django import forms

from odalc.users.forms import UserRegisterForm
from odalc.users.models import AdminUser


class AdminEditForm(forms.ModelForm):
    """Form class for editing admin user information."""
    class Meta:
        model = AdminUser
        fields = (
            'email',
            'first_name',
            'last_name'
        )


class AdminRegisterForm(UserRegisterForm):
    """Form class for adding a new admin user."""
    class Meta:
        model = AdminUser
        fields = (
            'email',
            'first_name',
            'last_name'
        )
