# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields
import odalc.users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacheruser',
            name='website',
            field=models.URLField(default='', max_length=255, verbose_name=b'Website', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='teacheruser',
            name='picture',
            field=imagekit.models.fields.ProcessedImageField(help_text=b'Please use a square image.', upload_to=odalc.users.models.picture_upload_path, verbose_name=b'Profile Picture'),
            preserve_default=True,
        ),
    ]
