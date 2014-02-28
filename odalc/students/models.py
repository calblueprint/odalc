from django.db import models

# Create your models here.

class CourseFeedback(models.Model):
	first_name = models.ForeignKey('StudentUser')
	course = models.ForeignKey('base.Course')

	encourage_questions = models.BooleanField()

	time_length_choices = ('too_long', 'Too Long'),('too_short','Too Short'),('just_right','Just Right')
	time_length = models.CharField(max_length=9, choices=time_length_choices)

	satisfaction = models.TextField()
	course_content = models.TextField()
	course_organization = models.TextField()
	teacher_delivery = models.TextField()
	classroom_facilities = models.TextField()
	useful_topics = models.TextField()
	other_topics = models.TextField()
