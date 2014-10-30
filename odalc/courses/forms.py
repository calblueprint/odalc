from datetime import datetime as dt

from django import forms

from odalc.courses.models import Course


class EditCourseForm(forms.ModelForm):
    date = forms.DateField(label='Date to Teach Course', required=False)
    start_time = forms.TimeField(label='Starting Time for Course Session', required=False)
    end_time = forms.TimeField(label='Ending Time for Course Session', required=False)

    def __init__(self, *args, **kwargs):
        super(EditCourseForm, self).__init__(*args, **kwargs)
        if self.instance.start_datetime:
            self.fields['date'].initial = self.instance.start_datetime.date
            self.fields['start_time'].initial = self.instance.start_datetime.time
        if self.instance.end_datetime:
            self.fields['end_time'].initial = self.instance.end_datetime.time

    def save(self, *args, **kwargs):
        date = self.cleaned_data.get('date')
        start_time = self.cleaned_data.get('start_time')
        end_time = self.cleaned_data.get('end_time')
        if date and start_time:
            self.instance.start_datetime = dt.combine(date, start_time)
        if date and end_time:
            self.instance.end_datetime = dt.combine(date, end_time)
        return super(EditCourseForm, self).save(*args, **kwargs)

    class Meta:
        model = Course
        exclude = (
            'teacher',
            'students',
            'start_datetime',
            'end_datetime',
            'is_featured'
            'image_thumbnail'
        )
