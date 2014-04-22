from django.db import models
from odalc.base.models import User
from localflavor.us import models as localflavor_models

# Create your models here.
class TeacherUser(User):
    INFO_SOURCE_FRIEND = 'FRD'
    INFO_SOURCE_WEB = 'WEB'
    INFO_SOURCE_OTHER = 'OTH'
    INFO_SOURCE_CHOICES = (
            (INFO_SOURCE_FRIEND, 'From a friend'),
            (INFO_SOURCE_WEB, 'Our website'),
            (INFO_SOURCE_OTHER, 'Other')
        )


    organization = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=255, blank=True)
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    zipcode = models.CharField(max_length=9, blank=True)
    phone = localflavor_models.PhoneNumberField()
    about = models.TextField()
    experience = models.TextField()
    #picture = models.ImageField(upload_to="teacher_picture_uploads")
    #resume = models.FileField(upload_to="teacher_resume_uploads")
    picture = models.URLField()
    resume = models.URLField()
    info_source = models.CharField(max_length=3, choices=INFO_SOURCE_CHOICES)

    class Meta:
        verbose_name = "Teacher"
