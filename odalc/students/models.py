from django.db import models
from django.contrib.auto import User

# Create your models here.
class StudentUser(User):

    class Meta:
        verbose_name = "Student"