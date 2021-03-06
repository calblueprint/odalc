import decimal
from random import randint
import os

from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand
from django.db import connection

from odalc.courses.models import Course, CourseAvailability, CourseFeedback
from odalc.users.models import AdminUser, StudentUser, TeacherUser

from sampledatahelper.helper import SampleDataHelper
from sampledatahelper.model_helper import ModelDataHelper

US='us'
DIR = os.path.dirname(os.path.abspath(__file__))

TEST_COURSE_IMAGE_PATH = 'sample/sample_course_pic.jpg'
TEST_TEACHER_IMAGE_PATH = 'sample/sample_headshot.jpg'
RANDOM_COURSE_IMAGE_PATH = 'sample/sample_course_%d.JPG'
RANDOM_TEACHER_IMAGE_PATH = 'sample/sample_headshot_%d.JPG'
TEST_PDF_PATH = 'sample/sample_pdf.pdf'

TEST_PDF_URL = 'https://s3.amazonaws.com/odalc-stage-media/sample/sample_pdf.pdf'
TEST_TEACHER_EMAIL = 'teacher@teacher.com'
TEST_STUDENT_EMAIL = 'student@student.com'
TEST_ADMIN_EMAIL = 'admin@admin.com'
TEST_PASSWORD = 'odalc'
COURSE_STATUS_CHOICES = [s[0] for s in Course.STATUS_CHOICES]
COURSE_SKILL_CHOICES = [s[0] for s in Course.SKILL_CHOICES]

class Command(BaseCommand):
    args = ''
    help = 'Generate seed data for models'
    sd = SampleDataHelper()
    md = ModelDataHelper()

    def generate_teachers(self, instances):
        cursor = connection.cursor()
        for x in range(instances):
            teacher = TeacherUser.objects.create(
                email=self.sd.email(),
                first_name=self.sd.name(locale=US),
                last_name=self.sd.surname(locale=US),
                organization=self.sd.words(1, 3),
                position=self.sd.words(1, 3),
                street_address=self.sd.number_string(3) + ' ' + self.sd.word() + ' St.',
                city='Berkeley',
                zipcode='94709',
                phone=self.sd.phone('es', 1),
                about=self.sd.paragraph(),
                experience=self.sd.paragraph(),
                info_source='WEB'
            )
            teacher.set_password(TEST_PASSWORD)
            teacher.save()
            cursor.execute('UPDATE users_teacheruser SET picture = %s, resume = %s WHERE user_ptr_id = %s', [RANDOM_TEACHER_IMAGE_PATH % randint(1,10), TEST_PDF_PATH, teacher.id])
        if not TeacherUser.objects.filter(email=TEST_TEACHER_EMAIL).exists():
            teacher = TeacherUser.objects.create(
                email=TEST_TEACHER_EMAIL,
                first_name='Awesome',
                last_name='Teacher',
                organization='Blueprint',
                position='President',
                street_address=self.sd.number_string(3) + ' ' + self.sd.word() + ' St.',
                city='Berkeley',
                zipcode='94709',
                phone=self.sd.phone('es', 1),
                about=self.sd.paragraph(),
                picture=TEST_TEACHER_IMAGE_PATH,
                experience=self.sd.paragraph(),
                info_source='WEB'
            )
            teacher.set_password(TEST_PASSWORD)
            teacher.save()
            cursor.execute('UPDATE users_teacheruser SET picture = %s, resume = %s WHERE user_ptr_id = %s', [TEST_TEACHER_IMAGE_PATH, TEST_PDF_PATH, teacher.id])
        return

    def generate_students(self, instances):
        for x in range(instances):
            student = StudentUser.objects.create(
                email=self.sd.email(),
                first_name=self.sd.name(locale=US),
                last_name=self.sd.surname(locale=US)
            )
            student.set_password(TEST_PASSWORD)
            student.save()
        if not StudentUser.objects.filter(email=TEST_STUDENT_EMAIL).exists():
            student = StudentUser.objects.create(
                email=TEST_STUDENT_EMAIL,
                first_name='STUDENT',
                last_name='ODALC'
            )
            student.set_password(TEST_PASSWORD)
            student.save()
        return

    def generate_admin(self):
        if not AdminUser.objects.filter(email=TEST_ADMIN_EMAIL).exists():
            admin = AdminUser.objects.create(
                email=TEST_ADMIN_EMAIL,
                first_name='ADMIN',
                last_name='ODALC'
            )
            admin.set_password(TEST_PASSWORD)
            admin.save()
        return

    def generate_courses(self, instances):
        # Generate 'Pending' Courses
        cursor = connection.cursor()
        for x in range(instances):
            student_qs = StudentUser.objects.all()
            course_students = []
            for x in range(6):
                s = self.sd.db_object_from_queryset(student_qs)
                course_students.append(s)
                student_qs = student_qs.exclude(pk=s.pk)
            course = Course(
                teacher=self.sd.db_object(TeacherUser),
                title=self.sd.words(1, 3),
                short_description=self.sd.words(15, 20),
                long_description=self.sd.paragraph(),
                size=self.sd.int(8, 10),
                start_datetime=self.sd.future_datetime(1000, 3000),
                end_datetime=self.sd.future_datetime(6000, 10000),
                prereqs=self.sd.words(3, 7),
                skill_level=self.sd.choice(COURSE_SKILL_CHOICES),
                cost=decimal.Decimal('6.00'),
                odalc_cost_split=decimal.Decimal('2.50'),
                additional_info=self.sd.paragraph(),
                status=Course.STATUS_PENDING
            )
            course.save()
            for s in course_students:
                course.students.add(s)
            course.save()
            cursor.execute('UPDATE courses_course SET image = %s, course_material = %s WHERE id = %s', [RANDOM_COURSE_IMAGE_PATH % randint(1,10), TEST_PDF_PATH, course.id])
        # Generate 'Accepted' Courses
        for x in range(instances):
            student_qs = StudentUser.objects.all()
            course_students = []
            for x in range(6):
                s = self.sd.db_object_from_queryset(student_qs)
                course_students.append(s)
                student_qs = student_qs.exclude(pk=s.pk)
            course = Course(
                teacher=self.sd.db_object(TeacherUser),
                title=self.sd.words(1, 3),
                short_description=self.sd.words(15, 20),
                long_description=self.sd.paragraph(),
                size=self.sd.int(8, 10),
                start_datetime=self.sd.future_datetime(1000, 3000),
                end_datetime=self.sd.future_datetime(6000, 10000),
                prereqs=self.sd.words(3, 7),
                skill_level=self.sd.choice(COURSE_SKILL_CHOICES),
                cost=decimal.Decimal('6.00'),
                odalc_cost_split=decimal.Decimal('2.50'),
                course_material=TEST_PDF_URL,
                additional_info=self.sd.paragraph(),
                status=Course.STATUS_ACCEPTED
            )
            course.save()
            for s in course_students:
                course.students.add(s)
            course.save()
            cursor.execute('UPDATE courses_course SET image = %s, course_material = %s WHERE id = %s', [RANDOM_COURSE_IMAGE_PATH % randint(1,10), TEST_PDF_PATH, course.id])
        # Generate 'Finished' Courses
        for x in range(instances):
            student_qs = StudentUser.objects.all()
            course_students = []
            for x in range(6):
                s = self.sd.db_object_from_queryset(student_qs)
                course_students.append(s)
                student_qs = student_qs.exclude(pk=s.pk)
            course = Course(
                teacher=self.sd.db_object(TeacherUser),
                title=self.sd.words(1, 3),
                short_description=self.sd.words(15, 20),
                long_description=self.sd.paragraph(),
                size=self.sd.int(8, 10),
                start_datetime=self.sd.past_datetime(1000, 3000),
                end_datetime=self.sd.past_datetime(6000, 10000),
                prereqs=self.sd.words(3, 7),
                skill_level=self.sd.choice(COURSE_SKILL_CHOICES),
                cost=decimal.Decimal('6.00'),
                odalc_cost_split=decimal.Decimal('2.50'),
                course_material=TEST_PDF_URL,
                additional_info=self.sd.paragraph(),
                status=Course.STATUS_FINISHED
            )
            course.save()
            for s in course_students:
                course.students.add(s)
            course.save()
            cursor.execute('UPDATE courses_course SET image = %s, course_material = %s WHERE id = %s', [RANDOM_COURSE_IMAGE_PATH % randint(1,10), TEST_PDF_PATH, course.id])
        # Generate 'Denied' Courses
        for x in range(instances):
            student_qs = StudentUser.objects.all()
            course_students = []
            for x in range(6):
                s = self.sd.db_object_from_queryset(student_qs)
                course_students.append(s)
                student_qs = student_qs.exclude(pk=s.pk)
            course = Course(
                teacher=self.sd.db_object(TeacherUser),
                title=self.sd.words(1, 3),
                short_description=self.sd.words(15, 20),
                long_description=self.sd.paragraph(),
                size=self.sd.int(8, 10),
                start_datetime=self.sd.past_datetime(1000, 3000),
                end_datetime=self.sd.past_datetime(6000, 10000),
                prereqs=self.sd.words(3, 7),
                skill_level=self.sd.choice(COURSE_SKILL_CHOICES),
                cost=decimal.Decimal('6.00'),
                odalc_cost_split=decimal.Decimal('2.50'),
                course_material=TEST_PDF_URL,
                additional_info=self.sd.paragraph(),
                status=Course.STATUS_DENIED
            )
            course.save()
            for s in course_students:
                course.students.add(s)
            course.save()
            cursor.execute('UPDATE courses_course SET image = %s WHERE id = %s', [RANDOM_COURSE_IMAGE_PATH % randint(1,10), course.id])

    def generate_course_feedback(self, instances):
        self.md.fill_model(CourseFeedback, instances)

    def generate_course_availability(self):
        courses = Course.objects.all()
        for course in courses:
            try:
                if course.courseavailability:
                    pass
            except CourseAvailability.DoesNotExist:
                avail = CourseAvailability(
                    course=course,
                    start_datetime1=self.sd.future_datetime(60, 1440),
                    end_datetime1=self.sd.future_datetime(1440, 2880),
                    start_datetime2=self.sd.future_datetime(2880, 4320),
                    end_datetime2=self.sd.future_datetime(4320, 5760),
                    start_datetime3=self.sd.future_datetime(7200, 8640),
                    end_datetime3=self.sd.future_datetime(10080, 11520)
                )
                avail.save()


    def handle(self, *args, **options):
        print "Generating Teachers..."
        self.generate_teachers(5)
        print "Generating Students..."
        self.generate_students(20)
        print "Generating Admins..."
        self.generate_admin()
        print "Generating Courses..."
        self.generate_courses(6)
        print "Generating Course Feedback..."
        self.generate_course_feedback(50)
        print "Generating Course Availabilities..."
        self.generate_course_availability()
        print "Done!"
