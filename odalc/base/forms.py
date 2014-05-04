from datetime import datetime as dt

from django import forms
from django.contrib.auth.models import Group, Permission
from django.utils.translation import ugettext as _

from odalc.base.models import Course, User
from odalc.odalc_admin.models import AdminUser
from odalc.students.models import StudentUser
from odalc.teachers.models import TeacherUser


class UserRegisterForm(forms.ModelForm):
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label=_("Password Confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification.")
    )

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            if type(user) == TeacherUser:
                try:
                    group = Group.objects.get(name='teachers')
                except Group.DoesNotExist:
                    group = Group(name="teachers")
                    group.save()
                    group.permissions.add(Permission.objects.get(codename="teacher_permission"))
            elif type(user) == StudentUser:
                try:
                    group = Group.objects.get(name='students')
                except Group.DoesNotExist:
                    group = Group(name="students")
                    group.save()
                    group.permissions.add(Permission.objects.get(codename="student_permission"))
            elif type(user) == AdminUser:
                try:
                    group = Group.objects.get(name='admins')
                except Group.DoesNotExist:
                    group = Group(name="admins")
                    group.save()
                    group.permissions.add(Permission.objects.get(codename="admin_permission"))
            else:
                raise Exception()
            user.save()
            group.user_set.add(user)
        return user


class EditCourseForm(forms.ModelForm):
    date = forms.DateField(label='Date to Teach Course', required=False)
    start_time = forms.TimeField(label='Starting Time for Course Session', required=False)
    end_time = forms.TimeField(label='Ending Time for Course Session', required=False)

    def save(self, *args, **kwargs):
        date = self.cleaned_data.get('date')
        start_time = self.cleaned_data.get('start_time')
        end_time = self.cleaned_data.get('end_time')
        if date and start_time:
            self.instance.start_datetime = dt.combine(date, start_time)
        if date and end_time:
            self.instance.end_datetime = dt.combine(date, end_time)
        return super(EditCourseForm, self).save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(EditCourseForm, self).__init__(*args, **kwargs)
        # TODO: Fix the timezones on these initial values
        if self.instance.start_datetime:
            self.fields['date'].initial = self.instance.start_datetime.date
            self.fields['start_time'].initial = self.instance.start_datetime.time
        if self.instance.end_datetime:
            self.fields['end_time'].initial = self.instance.end_datetime.time

    class Meta:
        model = Course
        exclude = ['teacher', 'students', 'start_datetime', 'end_datetime',]
