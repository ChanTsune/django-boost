from __future__ import annotations

from typing import Any

from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

__all__ = ["NonZeroValidator", "validate_non_zero"]


@deconstructible(path="django_boost.validators.NonZeroValidator")
class NonZeroValidator(BaseValidator):
    """Validate that an integer is not zero.

    Django's built-in validators cover the other integer ranges with
    ``MinValueValidator``/``MaxValueValidator``; excluding only zero is the
    one range they cannot express as a single validator.
    """

    message = _('Enter a non-zero integer.')
    code = 'non_zero'

    def __init__(self, message: Any = None) -> None:
        """Override the default message when one is given."""
        if message:
            self.message = message

    def __call__(self, value: Any) -> None:
        if value == 0:
            raise ValidationError(self.message, code=self.code)


non_zero_validator = NonZeroValidator()


def validate_non_zero(value: Any) -> None:
    return non_zero_validator(value)
