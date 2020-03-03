from django.forms import BooleanField, CharField

from django_boost.forms.widgets import (ColorInput, InvertCheckboxInput,
                                        PhoneNumberInput)
from django_boost.validators import validate_color_code

__all__ = ["ColorCodeField", "InvertBooleanField", "PhoneNumberField"]


class ColorCodeField(CharField):
    """
    Field for storing hexadecimal color code like ``#FFEEDD``.

    ::

      from django import forms
      from django_boost.forms.fields import ColorCodeField

      class MyForm(forms.Form):
          color = ColorCodeField()
    """

    widget = ColorInput
    default_validators = [validate_color_code]


class InvertBooleanField(BooleanField):
    """
    Field that returns inverted input.

    Returns false if the checkbox is checked, returns true if the checkbox is not checked.

    ::

      from django import forms
      from django_boost.forms.fields import InvertBooleanField

      class MyForm(forms.Form):
          invert = InvertBooleanField()
    """

    widget = InvertCheckboxInput


class PhoneNumberField(CharField):
    """
    Field for phone number.

    ::

      from django import forms
      from django_boost.forms.fields import PhoneNumberField

      class MyForm(forms.Form):
          phone = PhoneNumberField()
    """

    widget = PhoneNumberInput
