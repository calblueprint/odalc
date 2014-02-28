from django.db import models
from base import User

# Create your models here.
class Teacher(User):
    reviews = models.OneToManyField(Review, verbose_name="Reviews", null=True, blank=True)
    classes = models.OneToManyField(Class, verbose_name="Classes", null=True, blank=True)

    class Meta:
        verbose_name = "Teacher"

# class Review(models.Model):
#     instructor = models.ForeignKey("Teacher")
#     student = models.ForeignKey("Student")
#     course = models.ForeignKey("Course")
#     rating = models.IntegerField("Rating")
#     comments = models.TextField("Comments")
