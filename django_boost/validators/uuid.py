from __future__ import annotations

import uuid
import warnings

from django.core.exceptions import ValidationError

__all__ = ["validate_uuid4"]


def validate_uuid4(value: str) -> None:
    """Validate that `value` is a UUID4 string.

    Deprecated: raises a ``DeprecationWarning`` and will be removed in
    django-boost 4.0; validate UUIDs with Django's ``UUIDField`` or
    :func:`uuid.UUID` instead.
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
