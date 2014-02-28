from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class User(AbstractBaseUser):
    email = models.EmailField("Email", max_length=255, unique=True)
    name = models.CharField("Name", max_length=255)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'email']

    class Meta:
    	abstract = True