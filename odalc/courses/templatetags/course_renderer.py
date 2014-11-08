from urllib import urlencode
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter
@stringfilter
def to_list_elements(text):
    """ Converts a text to an HTML list, where list elements are separated by
    newlines in the text
    """
    ELEMENT_PATTERN = '<li>{0}</li>'
    return mark_safe("\n".join(
            map(lambda line: ELEMENT_PATTERN.format(line),
                filter(None, text.split('\n')))))


@register.simple_tag(takes_context=True)
def paginate_url(context, page_num):
    """ Utility for using Django's built-in pagination with other GET params
    """
    request = context.get('request')

    get_params = request.GET.copy()
    get_params['page'] = page_num
    url = request.path + "?" + urlencode({k: v for k,v in get_params.items()})

    return url
