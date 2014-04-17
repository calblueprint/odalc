from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required
from odalc.odalc_admin.views import ApplicationReviewView, AdminDashboardView

urlpatterns = patterns('',
    url(r'^review/(?P<pk>\d+)/$', permission_required('base.admin_permission')(ApplicationReviewView.as_view()), name='course_review'),
    url(r'^$', permission_required('base.admin_permission')(AdminDashboardView.as_view()), name='dashboard'),
)
