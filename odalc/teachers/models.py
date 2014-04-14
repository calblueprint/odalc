from django.db import models
from odalc.base.models import User
from localflavor.us import models as localflavor_models

# Create your models here.
class TeacherUser(User):
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    zipcode = models.CharField(max_length=9, blank=True)
    phone = localflavor_models.PhoneNumberField()
    about = models.TextField(blank=True)
    picture = models.ImageField(upload_to="teacher_picture_uploads")
    resume = models.FileField(upload_to="teacher_resume_uploads")
    experience = models.TextField(blank=True)

    info_source = models.CharField(max_length=11, choices=(('FFR', 'From a friend'),
                                                           ('WEB', 'Our website'),
                                                           ('OTH', 'Other')))

    class Meta:
        verbose_name = "Teacher"
