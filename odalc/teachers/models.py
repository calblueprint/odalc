from django.db import models
from base import User

# Create your models here.
class Teacher(User):
    street_address = models.CharField('Street Address', max_length=255, blank=True)
    city = models.CharField('City', max_length=255, blank=True)
    zipcode = models.IntegerField('ZIP Code', null=True, blank=True)
    phone = models.CharField('Phone', max_length=11, blank=True)
    about = models.TextField('About', blank=True)
    picture = models.ImageField('Picture', blank=True)
    resume = models.FilePathField('Resume', blank=True)
    experience = models.TextField('Experience', blank=True)
    
    info_source_choices = ('from_friend', 'From a friend'), ('website', 'Our website'), ('other', 'Other')
    info_source = models.TextField(choices=info_source_choices)


    class Meta:
        verbose_name = "Teacher"