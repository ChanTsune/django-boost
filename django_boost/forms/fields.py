from django.forms import BooleanField, CharField

from django_boost.forms.widgets import ColorInput, InvertCheckboxInput
from django_boost.validators import validate_color_code

__all__ = ["ColorCodeField", "InvertBooleanField"]

class ColorCodeField(CharField):
    """Field for storing hexadecimal color code like `FFEEDD`."""

    widget = ColorInput
    default_validators = [validate_color_code]


class InvertBooleanField(BooleanField):
    """Field that returns inverted input."""

    widget = InvertCheckboxInput
