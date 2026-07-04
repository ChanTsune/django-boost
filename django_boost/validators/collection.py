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
        self.elements = elements
        if message:
            self.message = message

    def __call__(self, value: Any) -> None:
        if not contain_any(value, self.elements):
            raise ValidationError(self.message % (self.elements,))
