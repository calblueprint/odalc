from django.conf.urls import patterns, include, url
from odalc.students.views import SubmitCourseFeedback

urlpatterns = patterns('',
	url(r'^$', SubmitCourseFeedback.as_view(), name='feedback')
)