"""This module collects validation functions and classes."""

from __future__ import annotations

import json
import uuid
import warnings
from collections.abc import Iterable
from json.decoder import JSONDecodeError
from typing import Any

from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator, RegexValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from .utils import contain_any


__all__ = ["validate_json", "validate_uuid4", "validate_color_code",
           "ContainAnyValidator"]


@deconstructible
class JsonValidator(BaseValidator):

    message = _('Enter valid JSON string.')
    code = 'json value'

    def __init__(self, message: Any = None) -> None:
        if message:
            self.message = message

    def __call__(self, value: Any) -> None:
        try:
            json.loads(value)
        except JSONDecodeError:
            raise ValidationError(self.message, code=self.code)


class ColorCodeValidator(RegexValidator):
    # Anchored: RegexValidator matches with regex.search(), so without \A..\Z
    # any string merely containing a color code (e.g. "x#abcdef") would pass.
    regex = r'\A#[0-9a-fA-F]{6}\Z'
    message = _('Enter 6-digit hexadecimal number including #.')


class ContainAnyValidator(BaseValidator):
    """Validate contain any of elements in input."""

    message = _('The input must contain one of "%s"\'s.')

    def __init__(self, elements: Iterable[Any], message: Any = None) -> None:
        self.elements = elements
        if message:
            self.message = message

    def __call__(self, value: Any) -> None:
        if not contain_any(value, self.elements):
            raise ValidationError(self.message % (self.elements,))


json_validator = JsonValidator()
color_code_validator = ColorCodeValidator()


def validate_json(value: str) -> None:
    return json_validator(value)


def validate_uuid4(value: str) -> None:
    """Deprecated UUID validator.

    Raises a ``DeprecationWarning`` and will be removed in django-boost 4.0;
    validate UUIDs with Django's ``UUIDField`` or :func:`uuid.UUID` instead.
    """
    warnings.warn(
        "'validate_uuid4' is deprecated and will be removed in django-boost"
        " 4.0; validate UUIDs with Django's 'UUIDField' or 'uuid.UUID' instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    try:
        uuid_value = uuid.UUID(value)
    except ValueError as e:
        raise ValidationError(str(e))
    if not uuid_value.hex == value.replace("-", ""):
        raise ValidationError("badly formed hexadecimal UUID string")


def validate_color_code(value: str) -> None:
    return color_code_validator(value)
