from django.conf.urls import patterns, include, url
from odalc.base.views import CourseDetailView
from odalc.students.views import SubmitCourseFeedbackView

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/feedback/$', SubmitCourseFeedbackView.as_view(), name='feedback'),
    url(r'^(?P<pk>\d+)/$', CourseDetailView.as_view(), name='detail'),
)