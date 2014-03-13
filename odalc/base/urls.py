from django.conf.urls import patterns, include, url
from odalc.base.views import CourseDetailView

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$', CourseDetailView.as_view(), name='detail'),
)
