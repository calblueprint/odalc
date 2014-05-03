from django.conf.urls import patterns, url
from django.contrib.auth.views import password_change

from odalc.teachers.views import (
    CreateCourseView,
    TeacherDashboardView,
    TeacherEditView,
    TeacherRegisterView,
)

urlpatterns = patterns('',
    url(r'^password_change/$',
        password_change,
        {
            'template_name': 'base/password_change.html',
            'post_change_redirect': 'teachers:dashboard'
        },
       name='password_change'
    ),
    url(r'^register/$', TeacherRegisterView.as_view(), name='register'),
    url(r'^edit/$', TeacherEditView.as_view(), name='edit'),
    url(r'^create/$', CreateCourseView.as_view(), name='create-course'),
    url(r'^dashboard/$', TeacherDashboardView.as_view(), name='dashboard'),
)
