from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.translation import gettext_lazy as _

from django_boost.utils import contain_any

__all__ = ["ContainAnyValidator"]


class ContainAnyValidator(BaseValidator):
    """Validate contain any of elements in input."""

    message = _('The input must contain one of "%s"\'s.')

    def __init__(self, elements: Iterable[Any], message: Any = None) -> None:
        # Set limit_value via BaseValidator so its __eq__ can compare validators.
        super().__init__(elements, message)

    def __call__(self, value: Any) -> None:
        if not contain_any(value, self.limit_value):
            message: Any = self.message
            try:
                message = message % (self.limit_value,)
            except TypeError:
                # A custom message may omit the %-placeholder; use it verbatim.
                pass
            raise ValidationError(message)
