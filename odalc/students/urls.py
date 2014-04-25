from django.conf.urls import patterns, include, url
from odalc.students.views import StudentRegisterView, StudentDashboardView, StudentEditView
from django.contrib.auth.views import password_change

urlpatterns = patterns('',
    url(r'^register/$', StudentRegisterView.as_view(), name='register'),
    url(r'^edit/$', StudentEditView.as_view(), name='edit'),
    url(r'^password_change/$', password_change, {'template_name': 'teachers/password_change.html',
                                                 'post_change_redirect': 'teachers:dashboard'})
    url(r'^$', StudentDashboardView.as_view(), name='dashboard'),
)
