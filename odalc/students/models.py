from django.db import models
from odalc.base.models import User

# Create your models here.
class StudentUser(User):

    class Meta:
        verbose_name = "Student"

class CourseFeedback(models.Model):
	student = models.ForeignKey('StudentUser')
	course = models.ForeignKey('base.Course')

	encourage_questions_choices = ('yes', 'Yes'),('no','No')
	encourage_questions = models.CharField(max_length=2, choices=encourage_questions_choices)

	time_length_choices = ('too_long', 'Too Long'),('too_short','Too Short'),('just_right','Just Right')
	time_length = models.CharField(max_length=9, choices=time_length_choices)

#Change these later when adding more multiple choice fields to the model
	multiple_choice_1 = models.CharField(max_length=255,)
	multiple_choice_2 = models.CharField(max_length=255,)
	multiple_choice_3 = models.CharField(max_length=255,)

	satisfaction = models.TextField('Overall Satisfaction:')
	course_content = models.TextField('Course Content:')
	course_organization = models.TextField('Course Organization:')
	teacher_delivery = models.TextField("Teacher's delivery")
	classroom_facilities = models.TextField('Classroom Facilities')
	useful_topics = models.TextField('Some of the most useful topics covered were:')
	other_topics = models.TextField('What other topics would you like to see offered?')
