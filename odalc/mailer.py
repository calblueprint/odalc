from django.core.mail import  EmailMultiAlternatives
from django.conf import settings
from django.template import Template, Context

from odalc.odalc_admin.models import AdminUser

import yaml

def send_odalc_email(template_name, context_dict, recipient_list, from_email=settings.EMAIL_HOST_USER, cc_admins=False):
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
    if 'html' in template_data[template_name]:
        html_template = Template(template_data[template_name]['html'])
    else: html_template = False
    subject = subject_template.render(context)
    body = body_template.render(context)
    if html_template:
        html_body = html_template.render(context)
    else: html_body = False

    if cc_admins:
        cc_list = AdminUser.objects.all().values_list('email', flat=True)
    else:
        cc_list = []
    email = EmailMultiAlternatives(subject=subject, body=body, from_email=from_email, to=recipient_list, cc=cc_list)
    if html_template:
        email.attach_alternative(html_body, "text/html")
    email.send()
