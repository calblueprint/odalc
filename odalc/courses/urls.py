from django.conf.urls import patterns, url
from odalc.courses.views import (
    CourseDetailView,
    CourseEditView,
    CourseListingView
)
from odalc.odalc_admin.views import CourseFeedbackView
from odalc.students.views import SubmitCourseFeedbackView

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/feedback/review/$', CourseFeedbackView.as_view(), name='feedback_review'),
    url(r'^(?P<pk>\d+)/feedback/$', SubmitCourseFeedbackView.as_view(), name='feedback'),
    url(r'^(?P<pk>\d+)/edit/$', CourseEditView.as_view(), name='edit'),
    url(r'^(?P<pk>\d+)/$', CourseDetailView.as_view(), name='detail'),
    url(r'^$', CourseListingView.as_view(), name='listing'),
)
