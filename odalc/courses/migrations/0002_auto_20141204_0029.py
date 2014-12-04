# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import odalc.courses.models
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(help_text=b'Banner image for your course page. Please use the highest resolution possible.', upload_to=odalc.courses.models.image_upload_path, verbose_name=b'Course Page Banner Image'),
            preserve_default=True,
        ),
    ]
