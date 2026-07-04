"""This module collects validation functions and classes."""

from __future__ import annotations

from django_boost.validators.collection import ContainAnyValidator
from django_boost.validators.color import (ColorCodeValidator,
                                           validate_color_code)
from django_boost.validators.integer import (NonZeroValidator,
                                             validate_non_zero)
from django_boost.validators.json import JsonValidator, validate_json
from django_boost.validators.uuid import validate_uuid4

__all__ = ["validate_json", "validate_uuid4", "validate_color_code",
           "validate_non_zero", "ContainAnyValidator", "NonZeroValidator",
           "ColorCodeValidator", "JsonValidator"]
