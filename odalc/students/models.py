from django.db import models
from odalc.base.models import User

# Create your models here.
class StudentUser(User):

    class Meta:
        verbose_name = "Student"

class CourseFeedback(models.Model):
    STRONGLY_DISAGREE = 1
    DISAGREE = 2
    NEITHER = 3
    AGREE = 4
    STRONGLY_AGREE = 5
    AGREEMENT_CHOICES = (
        (STRONGLY_AGREE, 'Strongly Agree'),
        (AGREE, 'Agree'),
        (NEITHER, 'Neither'),
        (DISAGREE, 'Disagree'),
        (STRONGLY_DISAGREE, 'Strongly Disagree'),
    )


    student = models.ForeignKey('StudentUser')
    course = models.ForeignKey('base.Course')

    knowledgeable_of_subject = models.IntegerField(
        'The instructor was knowledgeable of the subject matter.',
        choices=AGREEMENT_CHOICES
    )
    encourages_questions = models.IntegerField(
        'The instructor encouraged questions and/or discussion.',
        choices=AGREEMENT_CHOICES
    )
    teaching_effectiveness = models.IntegerField(
        'The instructor was effective in teaching the material.',
        choices=AGREEMENT_CHOICES
    )
    applicable_to_needs = models.IntegerField(
        'The course was applicable to my needs.',
        choices=AGREEMENT_CHOICES
    )
    would_recommend = models.IntegerField(
        'I would recommend this course to a friend.',
        choices=AGREEMENT_CHOICES
    )
    course_inspiring = models.IntegerField(
        'The course session was inspiring.',
        choices=AGREEMENT_CHOICES
    )
    other_topics = models.TextField(
        'Please provide any additional comments or suggestions about the course and/or the instructor.',
        blank=True
    )
