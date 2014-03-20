from django.conf.urls import patterns, include, url
from odalc.teachers.views import CreateCourse
from odalc.teachers.views import TeacherRegisteration

urlpatterns = patterns('',
    url(r'^register$', TeacherRegisteration.as_view(), name='register'),
    url(r'^create$', CreateCourse.as_view(), name='create-course'),
)
