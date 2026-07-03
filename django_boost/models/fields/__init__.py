from __future__ import annotations

import warnings

from django import forms
from django.db import models
from django.db.models.fields import CharField

from django_boost.forms import fields
from django_boost.models.fields.related_descriptors import (
    AutoReverseOneToOneDescriptor)
from django_boost.validators import validate_color_code


class ColorCodeField(CharField):
    """Field for storing hexadecimal color code like `FFEEDD`."""

    default_validators = [validate_color_code]

    def __init__(self, *args, upper=False, lower=False, **kwargs):
        kwargs.update({"max_length": 7})
        if upper and lower:
            raise AssertionError(
                'upper and lower can not be specified at the same time.'
                ' Please specify only one or the other.')
        self.upper = upper
        self.lower = lower
        if self.upper:
            self.normalize = self._upper_convert
        elif self.lower:
            self.normalize = self._lower_convert
        else:
            self.normalize = self._no_convert
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.upper:
            kwargs["upper"] = True
        if self.lower:
            kwargs["lower"] = True
        return name, path, args, kwargs

    def _upper_convert(self, value):
        return value.upper() if value is not None else value

    def _lower_convert(self, value):
        return value.lower() if value is not None else value

    def _no_convert(self, value):
        return value

    def pre_save(self, model_instance, add):
        return self.normalize(super().pre_save(model_instance, add))

    def to_python(self, value):
        return self.normalize(super().to_python(value))

    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': fields.ColorCodeField,
            **kwargs,
        })


class ColorCodeFiled(ColorCodeField):
    """Deprecated misspelled alias for :class:`ColorCodeField`.

    Retained for backward compatibility; instantiating it raises a
    ``DeprecationWarning`` and it will be removed in django-boost 4.0.
    """

    def __init__(self, *args, **kwargs):
        warnings.warn(
            "'ColorCodeFiled' is a deprecated misspelling of 'ColorCodeField'"
            " and will be removed in django-boost 4.0; use 'ColorCodeField'"
            " instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)


class SplitDateTimeField(models.DateTimeField):
    """
    A little convenient DateTimeField.

    form_class in django.db.models.DateTimeField is replaced with
    django.forms.SplitDateTimeField.
    The effect on DB is the same as django.db.models.DateTimeField.
    """

    def formfield(self, **kwargs):
        kwargs.update({'form_class': forms.SplitDateTimeField})
        return super().formfield(**kwargs)


class AutoOneToOneField(models.OneToOneField):
    """
    OneToOneField creates related object on first call if it doesn't exist yet.

    Use it instead of original OneToOne field.
    """

    related_accessor_class = AutoReverseOneToOneDescriptor
