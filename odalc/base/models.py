from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(email, first_name, last_name, password)
        user.save(using=self._db)
        return user


class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField("Email", max_length=255, unique=True)
    first_name = models.CharField("First Name", max_length=255)
    last_name = models.CharField("Last Name", max_length=255)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    @property
    def child(self):
        for related_object in self._meta.get_all_related_objects():
            if not issubclass(related_object.model, self.__class__):
                continue
            try:
                return getattr(self, related_object.get_accessor_name())
            except ObjectDoesNotExist:
                pass

    class Meta:
        permissions = (
            ("admin_permission", "Admin Permission"),
            ("teacher_permission", "Teacher Permission"),
            ("student_permission", "Student Permission")
        )


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
        validators=[MinValueValidator(5.00), MaxValueValidator(25.00)],
        help_text='Enrollment cost for students. We have a $5.00 minimum so that we can confirm commitment from students.'
    )
    odalc_cost_split = models.DecimalField(
        'Donate to Oakland Digital',
        max_digits=5,
        decimal_places=2,
        help_text='Amount of the enrollment cost you\'d like to donate to Oakland Digital.'
    )
    image = models.URLField(
        'Course Image',
        help_text='Image to use as the banner on the course page. Please use a high-resolution image if possible, but the Oakland Digital team can help find an appropriate image for this.'
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
