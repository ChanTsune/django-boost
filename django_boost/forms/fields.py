from django.forms import CharField, ChoiceField

from django_boost.forms.widgets import ColorInput, StarRateSelect
from django_boost.validators import validate_color_code


class ColorCodeField(CharField):
    """Field for storing hexadecimal color code like `FFEEDD`."""

    widget = ColorInput
    default_validators = [validate_color_code]


class StarField(ChoiceField):
    """Field for ranged integer"""
    widget = StarRateSelect
