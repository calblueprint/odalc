from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.views import password_change
from django.views.generic import TemplateView

from django.template import add_to_builtins
add_to_builtins('athumb.templatetags.thumbnail')

from odalc.base.views import (
    AboutPageView,
    DonatePageView,
    HomePageView
)
from odalc.lib.s3 import SignS3View

urlpatterns = patterns('',
    url(r'^admins/', include('odalc.odalc_admin.urls', namespace='admins')),
    url(r'^courses/', include('odalc.courses.urls', namespace='courses')),
    url(r'^students/', include('odalc.students.urls', namespace='students')),
    url(r'^teachers/', include('odalc.teachers.urls', namespace='teachers')),
    url(r'^users/', include('odalc.users.urls', namespace='users')),
    url(r'^about/$', AboutPageView.as_view(), name='about'),
    url(r'^donate/$', DonatePageView.as_view(), name='donate'),
    url(r'^sign_s3/$', SignS3View.as_view(), name='sign_s3'),
    url(r'^$', HomePageView.as_view(), name='home'),
)
