from datetime import datetime as dt
from itertools import chain
import os

from django.conf import settings
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator
)
from django.db import models

from odalc.users.models import StudentUser

from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill


class CourseManager(models.Manager):
    def get_featured(self, num_courses, qs=None):
        """ Get num_courses amount of featured courses. If we don't have enough
        featured courses, then we retrieve older ones
        """
        if qs is None:
            qs = super(CourseManager, self).get_queryset()
        featured_courses = qs.filter(
            is_featured = True).order_by('start_datetime')[:num_courses]
        # We don't have enough featured or upcoming courses, so show some past courses too
        if featured_courses.count() < num_courses:
            num_upcoming_needed = num_courses - featured_courses.count()
            upcoming_courses = qs.filter(status=Course.STATUS_ACCEPTED).exclude(
                is_featured=True).order_by('start_datetime')[:num_upcoming_needed]
            num_retrieved = upcoming_courses.count() + featured_courses.count()
            past_courses = []
            if num_retrieved < num_courses:
                past_courses = Course.objects.filter(
                    status=Course.STATUS_FINISHED
                ).order_by('-start_datetime')[:num_courses - num_retrieved]
            return list(chain(featured_courses, upcoming_courses, past_courses))
        # We have enough featured courses
        else:
            return featured_courses

    def get_all_approved(self, qs=None):
        if qs is None:
            qs = super(CourseManager, self).get_queryset()
        return qs.filter(
            models.Q(status=Course.STATUS_ACCEPTED) | models.Q(status=Course.STATUS_FINISHED)
        ).order_by('-start_datetime')

    def get_in_date_range(self, start, finish, qs=None):
        if qs is None:
            qs = super(CourseManager, self).get_queryset()
        return qs.filter(
            start_datetime__range=[start, finish],
            status=Course.STATUS_ACCEPTED
        ).order_by('start_datetime')

    def get_pending(self, qs=None):
        if qs is None:
            qs = super(CourseManager, self).get_queryset()
        return qs.filter(status=Course.STATUS_PENDING).order_by('-start_datetime')

    def get_active(self, is_featured=False, qs=None):
        """ Gets active courses, with a flag to specify if we want active featured
        courses or active non-featured courses """
        if qs is None:
            qs = super(CourseManager, self).get_queryset()
        return qs.filter(status=Course.STATUS_ACCEPTED, is_featured=is_featured).order_by('-start_datetime')

    def get_all_active(self, qs=None):
        if qs is None:
            qs = super(CourseManager, self).get_queryset()
        return qs.filter(status=Course.STATUS_ACCEPTED).order_by('-is_featured', '-start_datetime')

    def get_finished(self, qs=None):
        if qs is None:
            qs = super(CourseManager, self).get_queryset()
        return qs.filter(status=Course.STATUS_FINISHED).order_by('-start_datetime')

    def get_denied(self, qs=None):
        if qs is None:
            qs = super(CourseManager, self).get_queryset()
        return qs.filter(status=Course.STATUS_DENIED).order_by('-start_datetime')

    def approve_course(self, course, date, start_time, end_time):
        course.status = course.STATUS_ACCEPTED
        course.start_datetime = dt.combine(date, start_time)
        course.end_datetime = dt.combine(date, end_time)
        course.save()
        return course

    def deny_course(self, course):
        course.status = course.STATUS_DENIED
        course.save()
        return course

    def create_from_form(self, form, teacher):
        course = form.save(commit=False)
        course.teacher = teacher
        course.status = Course.STATUS_PENDING
        course.save()
        return course

    def toggle_featured(self, course_id, is_featured):
        course = Course.objects.get(id=course_id)
        course.is_featured = is_featured
        course.save()
        return course


class Course(models.Model):
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

    def image_upload_path(instance, filename):
        return os.path.join(
            str(instance.teacher.id) + '-' + instance.teacher.first_name + '-' + instance.teacher.last_name,
            'images',
            'course-picture-' + str(instance.id) + '-' + filename
        )

    def course_materials_upload_path(instance, filename):
        return os.path.join(
            str(instance.teacher.id) + '-' + instance.teacher.first_name + '-' + instance.teacher.last_name,
            'documents',
            'course-material-' + str(instance.id) + '-' + filename
        )

    teacher = models.ForeignKey('users.TeacherUser')
    students = models.ManyToManyField('users.StudentUser', blank=True)
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
        blank=True,
        help_text='Any skills, knowledge, or tools that students should be familiar with before enrolling. This will be displayed as a list, and you can separate list items using line breaks.',
        validators=[
            RegexValidator('^[^<>&]*$',
                message='Prerequisite text cannot include the characters <, >, or &.',
                code='invalid_prereqs'
            ),
        ]
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
    image = ProcessedImageField(
        upload_to=image_upload_path,
        processors=[ResizeToFill(1400, 600)],
        format='JPEG',
        options={'quality': 100}
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(300, 200)],
        format='JPEG',
        options={'quality': 75}
    )
    course_material = models.FileField(
        'Course Materials',
        upload_to=course_materials_upload_path,
        blank=True,
        null=True,
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

    objects = CourseManager()

    def get_cost_in_cents(self):
        return int(self.cost * 100)

    def get_num_open_seats(self):
        return self.size - self.students.count()

    def get_teacher_cost_split(self):
        return self.cost - self.odalc_cost_split

    def set_datetimes(self, date, start_time, end_time):
        self.start_datetime = dt.combine(date, start_time)
        self.end_datetime = dt.combine(date, end_time)
        self.save()
        return self

    def is_accepted(self):
        return self.status == Course.STATUS_ACCEPTED

    def is_finished(self):
        return self.status == Course.STATUS_FINISHED

    def is_full(self):
        return self.students.count() >= self.size

    def is_owner(self, teacher):
        return self.teacher == teacher

    def is_past_start_date(self, curr_datetime):
        if self.start_datetime:
            return curr_datetime.date() >= self.start_datetime.date()
        else:
            return False

    def is_student_in_course(self, student):
        return self.students.filter(id=student.id).exists()

    def is_student_feedback_submitted(self, student):
        return self.coursefeedback_set.filter(student=student.id).exists()


class CourseAvailabilityManager(models.Manager):
    def create_from_form_data(self, cleaned_data, course):
        start_datetime1 = dt.combine(
            cleaned_data.get('date1'),
            cleaned_data.get('start_time1')
        )
        start_datetime2 = dt.combine(
            cleaned_data.get('date2'),
            cleaned_data.get('start_time2')
        )
        start_datetime3 = dt.combine(
            cleaned_data.get('date3'),
            cleaned_data.get('start_time3')
        )
        end_datetime1 = dt.combine(
            cleaned_data.get('date1'),
            cleaned_data.get('end_time1')
        )
        end_datetime2 = dt.combine(
            cleaned_data.get('date2'),
            cleaned_data.get('end_time2')
        )
        end_datetime3 = dt.combine(
            cleaned_data.get('date3'),
            cleaned_data.get('end_time3')
        )
        return super(CourseAvailabilityManager, self).get_queryset().create(
            start_datetime1=start_datetime1,
            start_datetime2=start_datetime2,
            start_datetime3=start_datetime3,
            end_datetime1=end_datetime1,
            end_datetime2=end_datetime2,
            end_datetime3=end_datetime3,
            course=course
        )


class CourseAvailability(models.Model):
    course = models.OneToOneField('Course')
    start_datetime1 = models.DateTimeField()
    end_datetime1 = models.DateTimeField()
    start_datetime2 = models.DateTimeField()
    end_datetime2 = models.DateTimeField()
    start_datetime3 = models.DateTimeField()
    end_datetime3 = models.DateTimeField()

    objects = CourseAvailabilityManager()


class CourseFeedbackManager(models.Manager):
    def create_from_form(self, form, course_id, user_id):
        course_feedback = form.save(commit=False)
        course_feedback.course = Course.objects.get(id=course_id)
        course_feedback.student = StudentUser.objects.get(id=user_id)
        course_feedback.save()
        return course_feedback


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

    student = models.ForeignKey('users.StudentUser')
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

    objects = CourseFeedbackManager()

