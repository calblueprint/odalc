import os
import decimal

from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

from odalc.base.models import Course, CourseAvailability
from odalc.students.models import StudentUser, CourseFeedback
from odalc.teachers.models import TeacherUser
from odalc.odalc_admin.models import AdminUser
from sampledatahelper.helper import SampleDataHelper
from sampledatahelper.model_helper import ModelDataHelper

US='us'
DIR = os.path.dirname(os.path.abspath(__file__))
TEST_FILE_PATH = os.path.join(DIR,'blank.pdf')
TEST_IMAGE_PATH = os.path.join(DIR,'test.jpeg')
IMAGE_FILE = File(open(TEST_IMAGE_PATH))
TEST_FILE = File(open(TEST_FILE_PATH))
TEST_IMAGE_FILE = SimpleUploadedFile(IMAGE_FILE.name, IMAGE_FILE.file.read())
TEST_UPLOADED_FILE = SimpleUploadedFile(TEST_FILE.name, TEST_FILE.file.read())
TEST_TEACHER_EMAIL = 'teacher@teacher.com'
TEST_STUDENT_EMAIL = 'student@student.com'
TEST_ADMIN_EMAIL = 'admin@admin.com'
TEST_PASSWORD = 'odalc'
COURSE_STATUS_CHOICES = [s[0] for s in Course.STATUS_CHOICES]

class Command(BaseCommand):
    args = ''
    help = 'Generate seed data for ODALC models'
    sd = SampleDataHelper()
    md = ModelDataHelper()

    def generate_teachers(self, instances):
        for x in range(instances):
            teacher = TeacherUser.objects.create(
                email=self.sd.email(),
                first_name=self.sd.name(locale=US),
                last_name=self.sd.surname(locale=US),
                street_address=self.sd.number_string(3) + ' ' + self.sd.word() + ' St.',
                city='Berkeley',
                zipcode='94709',
                phone=self.sd.phone('es', 1),
                picture=self.sd.image(100,100),
                resume=TEST_UPLOADED_FILE,
                experience='Here is my experience',
                info_source='WEB'
            )
            teacher.set_password(TEST_PASSWORD)
            teacher.save()
        if not TeacherUser.objects.filter(email=TEST_TEACHER_EMAIL).exists():
            teacher = TeacherUser.objects.create(
                email=TEST_TEACHER_EMAIL,
                first_name='TEACHER',
                last_name='ODALC',
                street_address=self.sd.number_string(3) + ' ' + self.sd.word() + ' St.',
                city='Berkeley',
                zipcode='94709',
                phone=self.sd.phone('es', 1),
                picture=self.sd.image(100,100),
                resume=TEST_UPLOADED_FILE,
                experience='Here is my experience',
                info_source='WEB'
            )
            teacher.set_password(TEST_PASSWORD)
            teacher.save()
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
        for x in range(instances):
            student_qs = StudentUser.objects.all()
            course_students = []
            for x in range(3):
                s = self.sd.db_object_from_queryset(student_qs)
                course_students.append(s)
                student_qs = student_qs.exclude(pk=s.pk)
            course = Course(
                teacher=self.sd.db_object(TeacherUser),
                title=self.sd.words(1, 3),
                description=self.sd.paragraph(),
                size=self.sd.int(6, 10),
                start_datetime=self.sd.future_datetime(60, 1440),
                end_datetime=self.sd.future_datetime(1440, 2880),
                prereqs=self.sd.words(3, 7),
                skill_level=Course.SKILL_BEGINNER,
                cost=decimal.Decimal('6.00'),
                odalc_cost_split=decimal.Decimal('2.50'),
                image=self.sd.image(100,100),
                course_material=TEST_UPLOADED_FILE,
                additional_info=self.sd.paragraph(),
                status=self.sd.choice(COURSE_STATUS_CHOICES)
            )
            course.save()
            for s in course_students:
                course.students.add(s)
            course.save()

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
        self.generate_courses(5)
        print "Generating Course Feedback..."
        self.generate_course_feedback(10)
        print "Generating Course Availabilities..."
        self.generate_course_availability()
        print "Done!"
