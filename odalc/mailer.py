from django.core.mail import send_mail
from django.conf import settings
from django.template import Template, Context

import yaml

def send_odalc_emails(template_name, context_dict, recipient_list, sender=settings.DEFAULT_EMAIL):
    """ Templates for emails should be yaml files, with 'subject' and 'body' sections, so
    'template_name' should be something like 'foo'.

    'context_dict' should be just a Python dictionary of all the context variables you want
    available in the email templates (e.g. {'course': course, 'awesome_url': 'www.awesome.com'})

    'recipient_list' must be a list of email addresse strings we are sending to, even if it
    there is only one email in the list. On the other hand, 'from_address' is just one
    email address string.
    """
    with open(settings.EMAIL_TEMPLATES_PATH, 'r') as template:
        template_data = yaml.load(template)
    context = Context(context_dict)
    subject_template = Template(template_data[template_name]['subject'])
    body_template = Template(template_data[template_name]['body'])
    subject = subject_template.render(context)
    body = body_template.render(context)
    send_mail(subject, body, sender, recipient_list, fail_silently=False)
