from django.conf.urls import patterns, url
from odalc.odalc_admin.views import ApplicationReviewView, AdminDashboardView, AdminRegisterView

urlpatterns = patterns('',
    url(r'^review/(?P<pk>\d+)/$', ApplicationReviewView.as_view(), name='course_review'),
    url(r'^$', AdminDashboardView.as_view(), name='dashboard'),
    url(r'^register/$', AdminRegisterView.as_view(), name='register'),
)
