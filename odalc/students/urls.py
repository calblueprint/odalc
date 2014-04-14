from django.conf.urls import patterns, include, url
from odalc.students.views import StudentRegisterView, StudentDashboardView

urlpatterns = patterns('',
    url(r'^register$', StudentRegisterView.as_view(), name='register'),
    url(r'^$', StudentDashboardView.as_view(), name='student_dashboard'),
)