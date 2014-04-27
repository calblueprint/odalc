from django.conf.urls import patterns, include, url
from django.contrib.auth.views import password_change

from odalc.teachers.views import CreateCourse, TeacherRegisteration, TeacherEditView, TeacherDashboardView

urlpatterns = patterns('',
    url(r'^/password_change/',
        password_change,
        {
            'template_name': 'base/password_change.html',
            'post_change_redirect': 'teachers:dashboard'
        },
       name='password_change'
    ),
    url(r'^register/$', TeacherRegisteration.as_view(), name='register'),
    url(r'^edit/$', TeacherEditView.as_view(), name='edit'),
    url(r'^create/$', CreateCourse.as_view(), name='create-course'),
    url(r'^dashboard/$', TeacherDashboardView.as_view(), name='dashboard'),
)
