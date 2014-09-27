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
