from django.db import models
from django.contrib.auto import User

# Create your models here.
class Instructor(User):
    reviews = models.OneToManyField(Review, verbose_name="Reviews", null=True, blank=True)
    classes = models.OneToManyField(Class, verbose_name="Classes", null=True, blank=True)

    class Meta:
        verbose_name = "Instructor"

class Review(models.Model):
    instructor = models.ForeignKey("Instructor")
    student = models.ForeignKey("Student")
    course = models.ForeignKey("Course")
    rating = models.IntegerField("Rating")
    comments = models.TextField("Comments")
