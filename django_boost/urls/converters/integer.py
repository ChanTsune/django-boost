"""Extensions for Django's ``django.urls`` path converters."""

from __future__ import annotations

from typing import ClassVar


class BaseIntConverter:
    """Shared behavior for the signed-integer path converters.

    Each subclass only declares ``regex``; the regex alone decides which
    integers route, so an out-of-range value fails to match and 404s at the
    resolver instead of reaching the view. Parsing and reversing are common:
    the matched text is a valid integer literal, and reversing renders the
    canonical (``+``-free, unpadded) form.
    """

    regex: ClassVar[str]

    def to_python(self, value: str) -> int:
        return int(value)

    def to_url(self, value: int | str) -> str:
        return str(value)


class SignedIntConverter(BaseIntConverter):  # noqa: D101
    regex: ClassVar[str] = r'-?[0-9]+'


class PositiveIntConverter(BaseIntConverter):  # noqa: D101
    regex: ClassVar[str] = r'0*[1-9][0-9]*'


class NegativeIntConverter(BaseIntConverter):  # noqa: D101
    regex: ClassVar[str] = r'-0*[1-9][0-9]*'


class NonNegativeIntConverter(BaseIntConverter):  # noqa: D101
    regex: ClassVar[str] = r'[0-9]+'


class NonPositiveIntConverter(BaseIntConverter):  # noqa: D101
    regex: ClassVar[str] = r'0+|-0*[1-9][0-9]*'


class NonZeroIntConverter(BaseIntConverter):  # noqa: D101
    regex: ClassVar[str] = r'-?0*[1-9][0-9]*'
