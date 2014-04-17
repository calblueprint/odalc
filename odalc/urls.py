from django.conf.urls import patterns, include, url
from odalc.base.views import HomePageView
from odalc.base.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^admins/', include('odalc.odalc_admin.urls', namespace='admins')),
    url(r'^teachers/', include('odalc.teachers.urls', namespace='teachers')),
    url(r'^courses/', include('odalc.base.urls', app_name='base', namespace='courses')),
    url(r'^students/', include('odalc.students.urls', namespace='students')),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^$', HomePageView.as_view(), name='home'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
