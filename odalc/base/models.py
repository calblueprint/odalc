from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

# Create your models here.
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

    flyer = models.ImageField(upload_to='course_images')
    course_material = models.FileField(upload_to='course_material')

    additional_info = models.TextField(blank=True)