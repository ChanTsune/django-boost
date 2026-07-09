"""Extensions for Django's ``django.core.validators``."""

from __future__ import annotations

from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

__all__ = ["ColorCodeValidator", "validate_color_code"]


@deconstructible(path="django_boost.validators.ColorCodeValidator")
class ColorCodeValidator(RegexValidator):
    # Anchored: RegexValidator matches with regex.search(), so without \A..\Z
    # any string merely containing a color code (e.g. "x#abcdef") would pass.
    regex = r'\A#[0-9a-fA-F]{6}\Z'
    message = _('Enter 6-digit hexadecimal number including #.')


color_code_validator = ColorCodeValidator()


def validate_color_code(value: str) -> None:  # noqa: D103
    return color_code_validator(value)
