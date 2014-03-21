from django.db import models
from odalc.base.models import User

# Create your models here.
class AdminUser(User):

    class Meta:
        verbose_name = "Admin"