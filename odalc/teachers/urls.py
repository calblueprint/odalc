from django.conf.urls import patterns, include, url
from odalc.teachers.views import CreateCourse

urlpatterns = patterns('',
	url(r'^create$', CreateCourse.as_view(), name='create-course')
)