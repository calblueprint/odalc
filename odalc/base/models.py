from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

# Create your models here.
class Course(models.Model):
  teacher = models.ForeignKey('teachers.TeacherUser')
  students = models.ManyToManyField('students.StudentUser')
  
  title = models.CharField(max_length=50)
  description = models.TextField()
  size = models.IntegerField()
  start_datetime = models.DateTimeField(blank=True,null=True)
  end_datetime = models.DateTimeField(blank=True,null=True)
  
  prereqs = models.CharField(max_length=100)
  skill_level = models.CharField(max_length=25,choices=(('BEG','Beginner'),('INT','Intermediate'),('ADV','Advanced')))
  cost = models.DecimalField(max_digits=5,decimal_places=2,validators=[MinValueValidator(5.00)])
  odalc_cost_split = models.DecimalField(max_digits=5,decimal_places=2)

  need_flyer = models.BooleanField()  
  flyer = models.FileField(upload_to='Flyer Uploads')
  course_material = models.FileField(upload_to='Course Material')
  
  additional_info = models.TextField(blank=True)