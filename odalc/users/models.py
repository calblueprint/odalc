import os

from django.contrib.auth import models as auth_models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Group,
    PermissionsMixin
)
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save, post_syncdb
from django.dispatch import receiver

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from localflavor.us import models as localflavor_models


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(email, first_name, last_name, password)
        user.save(using=self._db)
        return user


class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField("Email", max_length=255, unique=True)
    first_name = models.CharField("First Name", max_length=255)
    last_name = models.CharField("Last Name", max_length=255)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    @property
    def child(self):
        for related_object in self._meta.get_all_related_objects():
            if not issubclass(related_object.model, self.__class__):
                continue
            try:
                return getattr(self, related_object.get_accessor_name())
            except ObjectDoesNotExist:
                pass


class AdminUser(User):
    class Meta:
        verbose_name = "Admin"


class StudentUser(User):
    class Meta:
        verbose_name = "Student"


class TeacherUser(User):
    INFO_SOURCE_FRIEND = 'From a friend'
    INFO_SOURCE_WEB = 'Our website'
    INFO_SOURCE_OTHER = 'Other'
    INFO_SOURCE_CHOICES = (
        (INFO_SOURCE_FRIEND, INFO_SOURCE_FRIEND),
        (INFO_SOURCE_WEB, INFO_SOURCE_WEB),
        (INFO_SOURCE_OTHER, 'Other (just type it in!)')
    )

    def picture_upload_path(instance, filename):
        return os.path.join(
            'uploads',
            str(instance.id) + '-' + instance.first_name + '-' + instance.last_name,
            'images',
            'profile-picture-' + filename
        )

    def resume_upload_path(instance, filename):
        return os.path.join(
            'uploads',
            str(instance.id) + '-' + instance.first_name + '-' + instance.last_name,
            'documents',
            'resume-' + filename
        )

    organization = models.CharField(
        'Organization',
        max_length=255,
        blank=True,
        help_text='Organization you are currently working at.'
    )
    position = models.CharField(
        'Position',
        max_length=255,
        blank=True,
        help_text='Position at this organization'
    )
    street_address = models.CharField(
        'Street Address',
        max_length=255,
        blank=True,
        help_text='You can enter your home or business address.',
    )
    city = models.CharField(
        'City',
        max_length=255,
        blank=True
    )
    zipcode = models.CharField(
        'ZIP Code',
        max_length=9,
        blank=True
    )
    phone = localflavor_models.PhoneNumberField(
        'Contact Number',
        help_text='Please use the most reliable phone number for contacting you.'
    )
    about = models.TextField(
        'About You',
        help_text='General bio about yourself. This will be shown on the course page.',
    )
    experience = models.TextField(
        'Professional Experience',
        help_text='Your professional experience. This wil also be shown on the course page.'
    )
    picture = ProcessedImageField(
        upload_to=picture_upload_path,
        processors=[ResizeToFill(600, 600)],
        format='JPEG',
        options={'quality': 100}
    )
    resume = models.FileField(
        'Resume',
        upload_to=resume_upload_path,
        help_text='Resumes should be in PDF format'
    )
    info_source = models.CharField(
        'How did you hear about us?',
        max_length=255,
        choices=INFO_SOURCE_CHOICES
    )

    class Meta:
        verbose_name = 'Teacher'


# On syncdb, create groups if they don't already exist
def create_groups(sender, **kwargs):
    Group.objects.get_or_create(name='odalc_admins')
    Group.objects.get_or_create(name='students')
    Group.objects.get_or_create(name='teachers')


post_syncdb.connect(create_groups, sender=auth_models)


@receiver(post_save, sender=AdminUser)
def add_to_odalc_admins_group(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='odalc_admins'))


@receiver(post_save, sender=StudentUser)
def add_to_students_group(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='students'))


@receiver(post_save, sender=TeacherUser)
def add_to_teachers_group(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='teachers'))
