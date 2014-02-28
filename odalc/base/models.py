from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class User(AbstractBaseUser):
    email = models.EmailField("Email", max_length=255, unique=True)
    first_name = models.CharField("First Name", max_length=255)
    last_name = models.CharField("Last_Name", max_length=255)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
    	abstract = True