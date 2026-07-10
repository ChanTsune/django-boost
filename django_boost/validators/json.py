"""Extensions for Django's ``django.core.validators``."""

from __future__ import annotations

import json
from json.decoder import JSONDecodeError
from typing import Any

from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

__all__ = ["JsonValidator", "validate_json"]


@deconstructible(path="django_boost.validators.JsonValidator")
class JsonValidator(BaseValidator):
    """Validate that the value is a JSON-parseable string."""

    message = _('Enter valid JSON string.')
    code = 'json value'

    def __init__(self, message: Any = None) -> None:
        """Override the default message when one is given."""
        if message:
            self.message = message

    def __call__(self, value: Any) -> None:
        try:
            json.loads(value)
        except JSONDecodeError:
            raise ValidationError(self.message, code=self.code)


json_validator = JsonValidator()


def validate_json(value: str) -> None:  # noqa: D103
    return json_validator(value)
