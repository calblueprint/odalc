# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import odalc.courses.models
import django.core.validators
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50, verbose_name=b'Course Title')),
                ('short_description', models.CharField(help_text=b'One or two sentences describing the course.', max_length=255, verbose_name=b'Short Description')),
                ('long_description', models.TextField(help_text=b'A full description of what the course will be about and what students will learn.', verbose_name=b'Long Description')),
                ('size', models.IntegerField(help_text=b'Number of students to open this course to. The recommended size is 6 to 8 people.', verbose_name=b'Course Size')),
                ('start_datetime', models.DateTimeField(null=True, verbose_name=b'Course Start Date/Time', blank=True)),
                ('end_datetime', models.DateTimeField(null=True, verbose_name=b'Course End Date/Time', blank=True)),
                ('prereqs', models.TextField(help_text=b'Any skills, knowledge, or tools that students should be familiar with before enrolling. This will be displayed as a list, and you can separate list items using line breaks.', verbose_name=b'Course Prerequisites', validators=[django.core.validators.RegexValidator(b'^[^<>&]*$', message=b'Prerequisite text cannot include the characters <, >, or &.', code=b'invalid_prereqs')])),
                ('skill_level', models.CharField(help_text=b'Skill level associated with this course.', max_length=12, verbose_name=b'Course Skill Level', choices=[(b'Beginner', b'Beginner'), (b'Intermediate', b'Intermediate'), (b'Advanced', b'Advanced')])),
                ('cost', models.DecimalField(help_text=b'Enrollment cost for students. We have a $5.00 minimum so that we can confirm commitment from students.', verbose_name=b'Course Fee', max_digits=5, decimal_places=2, validators=[django.core.validators.MinValueValidator(5.0), django.core.validators.MaxValueValidator(100.0)])),
                ('odalc_cost_split', models.DecimalField(help_text=b"Amount of the enrollment cost you'd like to donate to Oakland Digital. 100% of the proceeds go back to this program.", verbose_name=b'Donate to Oakland Digital', max_digits=5, decimal_places=2)),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=odalc.courses.models.image_upload_path)),
                ('course_material', models.FileField(help_text=b'Optional PDF of any course materials for students. This can include links to other materials as well. Only enrolled students will be able to see this link.', upload_to=odalc.courses.models.course_materials_upload_path, null=True, verbose_name=b'Course Materials', blank=True)),
                ('additional_info', models.TextField(help_text=b'Any additional information about the course.', verbose_name=b'Additional Information', blank=True)),
                ('status', models.CharField(default=b'PEN', max_length=3, verbose_name=b'Course Status', choices=[(b'PEN', b'Pending'), (b'ACC', b'Accepted'), (b'DEN', b'Denied'), (b'FIN', b'Finished')])),
                ('is_featured', models.BooleanField(default=False, verbose_name=b'Course Featured')),
                ('students', models.ManyToManyField(to='users.StudentUser', blank=True)),
                ('teacher', models.ForeignKey(to='users.TeacherUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseAvailability',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_datetime1', models.DateTimeField()),
                ('end_datetime1', models.DateTimeField()),
                ('start_datetime2', models.DateTimeField()),
                ('end_datetime2', models.DateTimeField()),
                ('start_datetime3', models.DateTimeField()),
                ('end_datetime3', models.DateTimeField()),
                ('course', models.OneToOneField(to='courses.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseFeedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('knowledgeable_of_subject', models.IntegerField(verbose_name=b'The instructor was knowledgeable of the subject matter.', choices=[(5, b'Strongly Agree'), (4, b'Agree'), (3, b'Neither'), (2, b'Disagree'), (1, b'Strongly Disagree')])),
                ('encourages_questions', models.IntegerField(verbose_name=b'The instructor encouraged questions and/or discussion.', choices=[(5, b'Strongly Agree'), (4, b'Agree'), (3, b'Neither'), (2, b'Disagree'), (1, b'Strongly Disagree')])),
                ('teaching_effectiveness', models.IntegerField(verbose_name=b'The instructor was effective in teaching the material.', choices=[(5, b'Strongly Agree'), (4, b'Agree'), (3, b'Neither'), (2, b'Disagree'), (1, b'Strongly Disagree')])),
                ('applicable_to_needs', models.IntegerField(verbose_name=b'The course was applicable to my needs.', choices=[(5, b'Strongly Agree'), (4, b'Agree'), (3, b'Neither'), (2, b'Disagree'), (1, b'Strongly Disagree')])),
                ('would_recommend', models.IntegerField(verbose_name=b'I would recommend this course to a friend.', choices=[(5, b'Strongly Agree'), (4, b'Agree'), (3, b'Neither'), (2, b'Disagree'), (1, b'Strongly Disagree')])),
                ('course_inspiring', models.IntegerField(verbose_name=b'The course session was inspiring.', choices=[(5, b'Strongly Agree'), (4, b'Agree'), (3, b'Neither'), (2, b'Disagree'), (1, b'Strongly Disagree')])),
                ('other_topics', models.TextField(verbose_name=b'Please provide any additional comments or suggestions about the course and/or the instructor.', blank=True)),
                ('course', models.ForeignKey(to='courses.Course')),
                ('student', models.ForeignKey(to='users.StudentUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
