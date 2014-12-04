from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.views import password_change
from django.views.generic import TemplateView

from odalc.base.views import (
    AboutPageView,
    DonatePageView,
    FaqPageView,
    HomePageView,
    TalentPageView,
    WorkPageView
)

urlpatterns = patterns('',
    url(r'^admins/', include('odalc.odalc_admin.urls', namespace='admins')),
    url(r'^courses/', include('odalc.courses.urls', namespace='courses')),
    url(r'^students/', include('odalc.students.urls', namespace='students')),
    url(r'^teachers/', include('odalc.teachers.urls', namespace='teachers')),
    url(r'^users/', include('odalc.users.urls', namespace='users')),
    url(r'^about/$', AboutPageView.as_view(), name='about'),
    url(r'^donate/$', DonatePageView.as_view(), name='donate'),
    url(r'^faq/$', FaqPageView.as_view(), name='faq'),
    url(r'^work/$', WorkPageView.as_view(), name='work'),
    url(r'^talent/$', TalentPageView.as_view(), name='talent'),
    url(r'^$', HomePageView.as_view(), name='home'),
)
