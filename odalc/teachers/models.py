from django.db import models

from odalc.base.models import User
from odalc.base.backends.upload import S3BotoStorage_ODALC

from localflavor.us import models as localflavor_models

from athumb.fields import ImageWithThumbsField
from athumb.backends.s3boto import S3BotoStorage_AllPublic

# Create your models here.
class TeacherUser(User):
    PUBLIC_MEDIA_BUCKET = S3BotoStorage_ODALC(bucket='odalc-stage-media-2')

    INFO_SOURCE_FRIEND = 'FRD'
    INFO_SOURCE_WEB = 'WEB'
    INFO_SOURCE_OTHER = 'OTH'
    INFO_SOURCE_CHOICES = (
        (INFO_SOURCE_FRIEND, 'From a friend'),
        (INFO_SOURCE_WEB, 'Our website'),
        (INFO_SOURCE_OTHER, 'Other')
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
        help_text='Please use the most reliable phone number for contacting you.')
    about = models.TextField(
        'About You',
        help_text='General bio about yourself. This will be shown on the course page.',
    )
    experience = models.TextField(
        'Professional Experience',
        help_text='Your professional experience. This wil also be shown on the course page.'
    )
    picture = ImageWithThumbsField(
        'Headshot',
        help_text='Please upload a square image.',
        upload_to="images/profiles",
        thumbs=(
            ('full', {'size': (600, 600)}),
        ),
        storage=PUBLIC_MEDIA_BUCKET
    )
    resume = models.URLField(
        'Resume',
        help_text='Resumes should be in PDF format'
    )
    info_source = models.CharField(
        'How did you hear about us?',
        max_length=255,
        choices=INFO_SOURCE_CHOICES
    )

    class Meta:
        verbose_name = 'Teacher'
