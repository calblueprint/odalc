from django.db import models
from base import User
from localflavor import us.models

# Create your models here.
class Teacher(User):
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    zipcode = models.CharField()
    phone = us.models.PhoneNumberField()
    about = models.TextField(blank=True)
    picture = models.ImageField(upload_to="Picture Uploads")
    resume = models.FileField(upload_to="Resume Uploads")
    experience = models.TextField(blank=True)

    info_source = models.CharField(max_length=11, choices=(('FFR', 'From a friend'),
                                                           ('WEB', 'Our website'),
                                                           ('OTH', 'Other')))


    class Meta:
        verbose_name = "Teacher"