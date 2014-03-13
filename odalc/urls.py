from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^students/', include('odalc.students.urls', namespace='students'))
)
