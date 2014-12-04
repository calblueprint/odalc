# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields
import odalc.users.models
import localflavor.us.models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name=b'Email')),
                ('first_name', models.CharField(max_length=255, verbose_name=b'First Name')),
                ('last_name', models.CharField(max_length=255, verbose_name=b'Last Name')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Admin',
            },
            bases=('users.user',),
        ),
        migrations.CreateModel(
            name='StudentUser',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Student',
            },
            bases=('users.user',),
        ),
        migrations.CreateModel(
            name='TeacherUser',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('organization', models.CharField(help_text=b'Organization you are currently working at.', max_length=255, verbose_name=b'Organization', blank=True)),
                ('position', models.CharField(help_text=b'Position at this organization', max_length=255, verbose_name=b'Position', blank=True)),
                ('street_address', models.CharField(help_text=b'You can enter your home or business address.', max_length=255, verbose_name=b'Street Address', blank=True)),
                ('city', models.CharField(max_length=255, verbose_name=b'City', blank=True)),
                ('zipcode', models.CharField(max_length=9, verbose_name=b'ZIP Code', blank=True)),
                ('phone', localflavor.us.models.PhoneNumberField(help_text=b'Please use the most reliable phone number for contacting you.', max_length=20, verbose_name=b'Contact Number')),
                ('about', models.TextField(help_text=b'General bio about yourself. This will be shown on the course page.', verbose_name=b'About You')),
                ('experience', models.TextField(help_text=b'Your professional experience. This wil also be shown on the course page.', verbose_name=b'Professional Experience')),
                ('picture', imagekit.models.fields.ProcessedImageField(upload_to=odalc.users.models.picture_upload_path)),
                ('resume', models.FileField(help_text=b'Resumes should be in PDF format', upload_to=odalc.users.models.resume_upload_path, verbose_name=b'Resume')),
                ('info_source', models.CharField(max_length=255, verbose_name=b'How did you hear about us?', choices=[(b'From a friend', b'From a friend'), (b'Our website', b'Our website'), (b'Other', b'Other (just type it in!)')])),
            ],
            options={
                'verbose_name': 'Teacher',
            },
            bases=('users.user',),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
            preserve_default=True,
        ),
    ]
