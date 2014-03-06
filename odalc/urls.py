from django.conf.urls import patterns, include, url
from odalc.students.views import SubmitCourseFeedback

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'odalc.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^students$', SubmitCourseFeedback.as_view(), name='feedback')
)
