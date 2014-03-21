import os, json
from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from django.template import Template, Context

EMAIL_TEMPLATES_PATH = os.path.join(settings.SETTINGS_PATH, 'templates', 'emails')
DEFAULT_EMAIL = 'odalc@odalc.org'

def send_odalc_emails(template_name, context_dict, recipient_list, sender=DEFAULT_EMAIL):
	with open(os.path.join(EMAIL_TEMPLATES_PATH, template_name), 'r') as template:
		template_data = json.load(template)
	context = Context(context_dict)
	subject_template = Template(template_data['subject'])
	body_template = Template(template_data['body'])
	subject = subject_template.render(context)
	body = body_template.render(context)
	send_mail(subject, body, sender, recipient_list, fail_silently=False)