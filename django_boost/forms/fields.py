from django.forms import CharField

from django_boost.forms.widgets import ColorInput
from django_boost.validators import validate_color_code


class ColorCodeField(CharField):
    """Field for storing hexadecimal color code like `FFEEDD`."""

    widget = ColorInput
    default_validators = [validate_color_code]
