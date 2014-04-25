from django.conf.urls import patterns, include, url
from odalc.students.views import StudentRegisterView, StudentDashboardView, StudentEditView

urlpatterns = patterns('',
    url(r'^register/$', StudentRegisterView.as_view(), name='register'),
    url(r'^edit/$', StudentEditView.as_view(), name='edit'),
    url(r'^$', StudentDashboardView.as_view(), name='dashboard'),
)
