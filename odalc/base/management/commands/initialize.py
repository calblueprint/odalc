from datetime import date, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand

from odalc.courses.models import Course
from odalc.users.models import AdminUser

class Command(BaseCommand):
    args = ''
    help = 'Initialize the project with a default odalc admin user'

    def handle(self, *args, **options):
        if not AdminUser.objects.filter(email=settings.INITIAL_ADMIN_EMAIL).exists():
            admin = AdminUser.objects.create(
                email=settings.INITIAL_ADMIN_EMAIL,
                first_name=settings.INITIAL_ADMIN_FIRST_NAME,
                last_name=settings.INITIAL_ADMIN_FIRST_NAME
            )
            admin.set_password(settings.INITIAL_ADMIN_PASSWORD)
            admin.save()
        return
