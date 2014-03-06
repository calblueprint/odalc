from django.conf.urls import patterns, include, url
from odalc.students.views import SubmitCourseFeedback

urlpatterns = patterns('',
	url(r'^feedback$', SubmitCourseFeedback.as_view(), name='feedback')
)