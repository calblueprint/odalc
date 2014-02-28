from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField("Email", max_length=255, unique=True)
    password = None

    class Meta:
    	abstract = True