from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required
from odalc.odalc_admin.views import ApplicationReviewView, AdminDashboardView

urlpatterns = patterns('',
    url(r'^review/(?P<pk>\d+)/$', ApplicationReviewView.as_view(), name='course_review'),
    url(r'^$', AdminDashboardView.as_view(), name='dashboard'),
)
