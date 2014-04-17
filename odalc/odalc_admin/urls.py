from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import permission_required
from odalc.odalc_admin.views import ApplicationReviewView

urlpatterns = patterns('',
    url(r'^review/(?P<pk>\d+)/$', permission_required('base.admin_permission')(ApplicationReviewView.as_view()), name='course_review'),
)

