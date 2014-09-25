from django.conf import settings
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)
from django.db import models

from odalc.base.backends.upload import S3BotoStorage_ODALC

from athumb.fields import ImageWithThumbsField
from athumb.backends.s3boto import S3BotoStorage_AllPublic


class Course(models.Model):
    PUBLIC_MEDIA_BUCKET = S3BotoStorage_ODALC(bucket=settings.S3_BUCKET)

    SKILL_BEGINNER = 'Beginner'
    SKILL_INTERMEDIATE = 'Intermediate'
    SKILL_ADVANCED = 'Advanced'

    SKILL_CHOICES = (
        (SKILL_BEGINNER, SKILL_BEGINNER),
        (SKILL_INTERMEDIATE, SKILL_INTERMEDIATE),
        (SKILL_ADVANCED, SKILL_ADVANCED)
    )

    STATUS_PENDING = 'PEN'
    STATUS_ACCEPTED = 'ACC'
    STATUS_DENIED = 'DEN'
    STATUS_FINISHED = 'FIN'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_DENIED, 'Denied'),
        (STATUS_FINISHED, 'Finished')
    )

    teacher = models.ForeignKey('teachers.TeacherUser')
    students = models.ManyToManyField('students.StudentUser', blank=True)
    title = models.CharField('Course Title', max_length=50)
    short_description = models.CharField(
        'Short Description',
        max_length=255,
        help_text='One or two sentences describing the course.'
    )
    long_description = models.TextField(
        'Long Description',
        help_text='A full description of what the course will be about and what students will learn.',
    )
    size = models.IntegerField(
        'Course Size',
        help_text='Number of students to open this course to. The recommended size is 6 to 8 people.',
    )
    start_datetime = models.DateTimeField(
        'Course Start Date/Time',
        blank=True,
        null=True
    )
    end_datetime = models.DateTimeField(
        'Course End Date/Time',
        blank=True,
        null=True
    )
    prereqs = models.TextField(
        'Course Prerequisites',
        help_text='Any skills, knowledge, or tools that students should be familiar with before enrolling.'
    )
    skill_level = models.CharField(
        'Course Skill Level',
        max_length=12,
        choices=SKILL_CHOICES,
        help_text='Skill level associated with this course.'
    )
    cost = models.DecimalField(
        'Course Fee',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(5.00), MaxValueValidator(50.00)],
        help_text='Enrollment cost for students. We have a $5.00 minimum so that we can confirm commitment from students.'
    )
    odalc_cost_split = models.DecimalField(
        'Donate to Oakland Digital',
        max_digits=5,
        decimal_places=2,
        help_text='Amount of the enrollment cost you\'d like to donate to Oakland Digital. 100% of the proceeds go back to this program.'
    )
    image = ImageWithThumbsField(
        'Course Image',
        help_text='Image to use as the banner on the course page. Please use a high-resolution image if possible, but the Oakland Digital team can help find an appropriate image for this.',
        upload_to="images/courses",
        thumbs=(
            ('thumb', {'size': (300, 200), 'crop': True}),
            ('full', {'size': (1400, 500), 'crop': True}),
        ),
        storage=PUBLIC_MEDIA_BUCKET
    )
    course_material = models.URLField(
        'Course Materials',
        blank=True,
        help_text='Optional PDF of any course materials for students. This can include links to other materials as well. Only enrolled students will be able to see this link.'
    )
    additional_info = models.TextField(
        'Additional Information',
        blank=True,
        help_text='Any additional information about the course.',
    )
    status = models.CharField(
        'Course Status',
        max_length=3,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )
    is_featured = models.BooleanField(
        'Course Featured',
        default=False
    )


class CourseAvailability(models.Model):
    course = models.OneToOneField('Course')
    start_datetime1 = models.DateTimeField()
    end_datetime1 = models.DateTimeField()
    start_datetime2 = models.DateTimeField()
    end_datetime2 = models.DateTimeField()
    start_datetime3 = models.DateTimeField()
    end_datetime3 = models.DateTimeField()


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

    student = models.ForeignKey('students.StudentUser')
    course = models.ForeignKey('Course')

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
