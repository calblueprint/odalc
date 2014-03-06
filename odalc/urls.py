from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^teachers/', include('odalc.teachers.urls', namespace='teachers'))

)
