from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Course(models.Model):
  teacher = models.ForeignKey(TeacherUser)
  students = models.ManyToMany(StudentUsers)
  
  title = models.CharField(max_length=50)
  description = models.CharField(max_length=250)
  size = models.IntegerField()
  start_datetime = models.DateTimeField(blank=True,null=True)
  end_datetime = models.DateTimeField(blank=True,null=True)
  
  prereqs = models.CharField(max_length=100)
  skill_level = models.CharField(choices=(('Beginner','Beginner'),('Intermediate','Intermediate'),('Advanced','Advanced')))
  cost = models.FloatField(validators=MinValueValidator(5.00))
  odalc_cost_split = models.FloatField()

  need_flyer = models.BooleanField()  
  flyer = 
  course_material = 
  
  additional_info = models.CharField()
  

  
