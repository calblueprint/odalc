from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.core.validators import MinValueValidator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group, Permission

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
    SKILL_BEGINNER = 'BEG'
    SKILL_INTERMEDIATE = 'INT'
    SKILL_ADVANCED = 'ADV'

    SKILL_CHOICES = (
        (SKILL_BEGINNER,'Beginner'),
        (SKILL_INTERMEDIATE,'Intermediate'),
        (SKILL_ADVANCED,'Advanced')
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
    students = models.ManyToManyField('students.StudentUser',blank=True)
    title = models.CharField(max_length=50)
    short_description = models.CharField(max_length=255)
    long_description = models.TextField()
    size = models.IntegerField()
    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)
    prereqs = models.TextField()
    skill_level = models.CharField(max_length=3, choices=SKILL_CHOICES)
    cost = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(5.00)]
    )
    odalc_cost_split = models.DecimalField(max_digits=5, decimal_places=2)
    #image = models.ImageField(upload_to='course_images')
    #course_material = models.FileField(upload_to='course_material')
    image = models.URLField()
    course_material = models.URLField()
    additional_info = models.TextField(blank=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=STATUS_PENDING)


class CourseAvailability(models.Model):
    course = models.OneToOneField('Course')

    start_datetime1 = models.DateTimeField(blank=True,null=True)
    end_datetime1 = models.DateTimeField(blank=True,null=True)

    start_datetime2 = models.DateTimeField(blank=True,null=True)
    end_datetime2 = models.DateTimeField(blank=True,null=True)

    start_datetime3 = models.DateTimeField(blank=True,null=True)
    end_datetime3 = models.DateTimeField(blank=True,null=True)
