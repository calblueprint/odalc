from django.db import models

# Create your models here.

class CourseFeedback(models.Model):
	first_name = models.ForeignKey('StudentUser')
	course = models.ForeignKey('Course')

	encourage_questions = models.BooleanField()

	time_length_choices = ('too_long', 'Too Long'),('too_short','Too Short'),('just_right','Just Right')
	time_length = models.CharField(choices=time_length_choices)

	satisfaction = models.CharField(max_length=1000,)
	course_content = models.CharField(max_length=1000,)
	course_organization = models.CharField(max_length=1000,)
	teacher_delivery = models.CharField(max_length=1000,)
	classroom_facilities = models.CharField(max_length=1000,)
	useful_topics = models.CharField(max_length=1000,)
	other_topics = models.CharField(max_length=1000,)
