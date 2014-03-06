from django.views.generic import DetailView, TemplateView
from odalc.base.models import Course

# Create your views here.

class CourseView(DetailView):
	model = Course
	context_object_name = 'course'
	template_name = 'base/course.html'

	def get_context_data(self, **kwargs):
		context = super(CourseView, self).get_context_data(**kwargs)
		return context 


class HomePageView(TemplateView):
	template_name = 'base/home.html'
