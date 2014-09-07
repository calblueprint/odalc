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
    HomePageView,
    LoginView,
    LogoutView,
    SignS3View
)

urlpatterns = patterns('',
    url(r'^admins/', include('odalc.odalc_admin.urls', namespace='admins')),
    url(r'^teachers/', include('odalc.teachers.urls', namespace='teachers')),
    url(r'^courses/', include('odalc.base.urls', app_name='base', namespace='courses')),
    url(r'^students/', include('odalc.students.urls', namespace='students')),
    url(r'^accounts/login/', LoginView.as_view(), name='login'),
    url(r'^accounts/logout/', LogoutView.as_view(), name='logout'),
    url(r'^about/', AboutPageView.as_view(), name='about'),
    url(r'^donate/', DonatePageView.as_view(), name='donate'),
    url(r'^coursepage/', TemplateView.as_view(template_name='mockups/course_page.html'), name='course_mock'),
    url(r'^sign_s3/', SignS3View.as_view(), name='sign_s3'),
    url(r'^$', HomePageView.as_view(), name='home'),
)
