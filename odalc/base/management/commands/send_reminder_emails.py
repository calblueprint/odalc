from datetime import date, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse

from odalc.courses.models import Course
from odalc.lib.mailer import send_odalc_email

class Command(BaseCommand):
    args = ''
    help = 'Sends a reminder email about a course to enrolled students and the teacher the day before the session'

    def handle(self, *args, **options):
        courses_next_day = Course.objects.filter(start_datetime__range=[date.today()+timedelta(days=1), date.today()+timedelta(days=2)])
        for course in courses_next_day:
            context = {
                'course': course,
                'course_url': settings.SITE_URL + reverse('courses:detail', args=(course.id,)),
                'course_date': course.start_datetime.strftime('%A, %B %d'),
                'course_start_time': course.start_datetime.strftime('%I:%M %p'),
                'course_end_time': course.end_datetime.strftime('%I:%M %p'),
            }
            student_email_list = list(course.students.values_list('email', flat=True))
            send_odalc_email('remind_teacher', context, [course.teacher.email], cc_admins=True)
            send_odalc_email('remind_students', context, student_email_list)
