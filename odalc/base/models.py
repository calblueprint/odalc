from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.core.validators import MinValueValidator

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

class User(AbstractBaseUser):
    email = models.EmailField("Email", max_length=255, unique=True)
    first_name = models.CharField("First Name", max_length=255)
    last_name = models.CharField("Last_Name", max_length=255)

    USERNAME_FIELD = 'email'

    objects = UserManager()

class Course(models.Model):
    SKILL_CHOICES = (
        ('BEG','Beginner'),
        ('INT','Intermediate'),
        ('ADV','Advanced')
    )

    teacher = models.ForeignKey('teachers.TeacherUser')
    students = models.ManyToManyField('students.StudentUser',blank=True)

    title = models.CharField(max_length=50)
    description = models.TextField()
    size = models.IntegerField()
    start_datetime = models.DateTimeField(blank=True,null=True)
    end_datetime = models.DateTimeField(blank=True,null=True)

    prereqs = models.TextField()
    skill_level = models.CharField(max_length=25,choices=SKILL_CHOICES)
    cost = models.DecimalField(max_digits=5,decimal_places=2,validators=[MinValueValidator(5.00)])
    odalc_cost_split = models.DecimalField(max_digits=5,decimal_places=2)

    image = models.ImageField(upload_to='course_images')
    course_material = models.FileField(upload_to='course_material')

    additional_info = models.TextField(blank=True)


class CourseAvailability(models.Model):
    course = models.OneToOneField('Course')

    start_datetime1 = models.DateTimeField(blank=True,null=True)
    end_datetime1 = models.DateTimeField(blank=True,null=True)

    start_datetime2 = models.DateTimeField(blank=True,null=True)
    end_datetime2 = models.DateTimeField(blank=True,null=True)

    start_datetime3 = models.DateTimeField(blank=True,null=True)
    end_datetime3 = models.DateTimeField(blank=True,null=True)
