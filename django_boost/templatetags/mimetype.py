from mimetypes import guess_type

from django.template import Library

register = Library()


@register.filter(name="mimetype")
def mimetype(value):
    if "." not in value:
        value = "." + value
    if value.startswith("."):
        value = "s" + value
    return guess_type(value)[0]
