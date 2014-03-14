from django.conf.urls import patterns, include, url
from odalc.odalc_admin.views import ApplicationReviewView

urlpatterns = patterns('',
    url(r'^review/(?P<pk>\d+)/$', ApplicationReviewView.as_view(), name='course_review'),
)