from django.conf.urls import patterns, include, url
from odalc.teachers.views import CreateCourse, TeacherRegisteration, TeacherDashboardView

urlpatterns = patterns('',
    url(r'^register$', TeacherRegisteration.as_view(), name='register'),
    url(r'^create$', CreateCourse.as_view(), name='create-course'),
    url(r'^dashboard$', TeacherDashboardView.as_view(), name='dashboard'),
)
