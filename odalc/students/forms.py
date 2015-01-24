from django import forms

from odalc.courses.models import CourseFeedback
from odalc.users.forms import UserRegisterForm
from odalc.users.models import StudentUser


class StudentRegisterForm(UserRegisterForm):
    """Form class for new student users."""
    class Meta:
        model = StudentUser
        fields = ('email', 'first_name', 'last_name')


class StudentEditForm(forms.ModelForm):
    """Form class for editing student users."""
    class Meta:
        model = StudentUser
        fields = ('email', 'first_name', 'last_name')


class FeedbackForm(forms.ModelForm):
    """Form class for CourseFeedback model."""
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['knowledgeable_of_subject'].widget = forms.RadioSelect(choices=CourseFeedback.AGREEMENT_CHOICES)
        self.fields['encourages_questions'].widget = forms.RadioSelect(choices=CourseFeedback.AGREEMENT_CHOICES)
        self.fields['teaching_effectiveness'].widget = forms.RadioSelect(choices=CourseFeedback.AGREEMENT_CHOICES)
        self.fields['applicable_to_needs'].widget = forms.RadioSelect(choices=CourseFeedback.AGREEMENT_CHOICES)
        self.fields['would_recommend'].widget = forms.RadioSelect(choices=CourseFeedback.AGREEMENT_CHOICES)
        self.fields['course_inspiring'].widget = forms.RadioSelect(choices=CourseFeedback.AGREEMENT_CHOICES)

    class Meta:
        model = CourseFeedback
        exclude = ['course', 'student']
