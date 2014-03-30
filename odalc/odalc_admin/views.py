from django.views.generic import UpdateView
from odalc.base.models import Course

# Create your views here.

class ApplicationReviewView(UpdateView):
	model = Course
	fields = [
		'title',
		'description',
		'size',
		'start_datetime',
		'end_datetime',
		'prereqs',
		'skill_level',
		'cost',
		'odalc_cost_split',
		'image',
		'additional_info'
	]
	context_object_name = 'course'
	template_name = 'odalc_admin/course_application_review.html'

	def get_context_data(self, **kwargs):
		context = super(ApplicationReviewView, self).get_context_data(**kwargs)
		return context 