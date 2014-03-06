from django import forms
from django.core.exceptions import ValidationError

from odalc.students.models import CourseFeedback

class FeedbackForm(forms.ModelForm):
	class Meta:
		model = CourseFeedback
		exclude = ['course', 'student']