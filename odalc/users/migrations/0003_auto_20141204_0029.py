# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20141204_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacheruser',
            name='info_source',
            field=models.CharField(max_length=255, verbose_name=b'How did you hear about us?', choices=[(b'From a friend', b'From a friend'), (b'Our website', b'Our website'), (b'Other', b'Other')]),
            preserve_default=True,
        ),
    ]
