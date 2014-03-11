from django.conf.urls import patterns, include, url
from odalc.teachers.views import TeacherRegisteration

urlpatterns = patterns('',
	url(r'register$', TeacherRegisteration.as_view(), name='register')
)