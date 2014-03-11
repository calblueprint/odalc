from django.conf.urls import patterns, include, url
from odalc.students.views import StudentRegisterView

urlpatterns = patterns('',
	url(r'register$', StudentRegisterView.as_view(), name='register')
)