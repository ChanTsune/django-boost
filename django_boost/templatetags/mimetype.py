"""This module provides mimetypes utility for django template."""

from __future__ import annotations

from mimetypes import guess_type

from django.template import Library

register = Library()


@register.filter(name="mimetype")
def mimetype(value):
    """Guess a MIME type from a bare extension, a leading-dot extension, or a full filename."""
    if "." not in value:
        value = "." + value
    if value.startswith("."):
        value = "s" + value
    return guess_type(value)[0]
