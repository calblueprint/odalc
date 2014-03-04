from django.db import models
from base import User

# Create your models here.
class StudentUser(User):

    class Meta:
        verbose_name = "Student"