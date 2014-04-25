from django.conf.urls import patterns, include, url
from odalc.teachers.views import CreateCourse, TeacherRegisteration, TeacherEditView, TeacherDashboardView
from django.contrib.auth.views import password_change

urlpatterns = patterns('',
    url(r'^register/$', TeacherRegisteration.as_view(), name='register'),
    url(r'^edit/$', TeacherEditView.as_view(), name='edit'),
    url(r'^password_change/$', password_change, {'template_name': 'teachers/password_change.html', 'post_change_redirect': 'teachers:dashboard'}),
    url(r'^create/$', CreateCourse.as_view(), name='create-course'),
    url(r'^dashboard/$', TeacherDashboardView.as_view(), name='dashboard'),
)
