from django.template import Library

from django_boost.contrib.qrcode.utils import base64_string_qrcode

register = Library()

def qrcode(data, level=None):
    return base64_string_qrcode(data)
