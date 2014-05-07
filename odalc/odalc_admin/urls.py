from django.conf.urls import patterns, url
from django.contrib.auth.views import password_change

from odalc.odalc_admin.views import (
    ApplicationReviewView,
    AdminDashboardView,
    AdminEditView,
    AdminRegisterView
)

urlpatterns = patterns('',
    url(r'^password_change/$',
        password_change,
        {
            'template_name': 'odalc_admin/password_change.html',
            'post_change_redirect': 'admins:dashboard'
        },
        name='password_change',
    ),
    url(r'^edit/$', AdminEditView.as_view(), name='edit'),
    url(r'^register/$', AdminRegisterView.as_view(), name='register'),
    url(r'^review/(?P<pk>\d+)/$', ApplicationReviewView.as_view(), name='course_review'),
    url(r'^$', AdminDashboardView.as_view(), name='dashboard'),
)
