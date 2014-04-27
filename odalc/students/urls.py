from django.conf.urls import patterns, include, url
from django.contrib.auth.views import password_change

from odalc.students.views import StudentRegisterView, StudentDashboardView, StudentEditView

urlpatterns = patterns('',
    url(r'^/password_change/',
        password_change,
        {
            'template_name': 'base/password_change.html',
            'post_change_redirect': 'students:dashboard'
        },
       name='password_change'
    ),
    url(r'^register/$', StudentRegisterView.as_view(), name='register'),
    url(r'^edit/$', StudentEditView.as_view(), name='edit'),
    url(r'^$', StudentDashboardView.as_view(), name='dashboard'),
)
