from django import forms

from odalc.odalc_admin.models import AdminUser

class AdminEditForm(forms.ModelForm):
    class Meta:
        model = AdminUser
        fields = (
            'email',
            'first_name',
            'last_name',
        )
