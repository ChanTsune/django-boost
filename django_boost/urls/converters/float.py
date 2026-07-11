"""Extensions for Django's ``django.urls`` path converters."""

from __future__ import annotations

from typing import ClassVar

from django_boost.urls.converters._numeric import (
    BaseSignedNumericConverter, POSITIVE, ZERO)


class BaseFloatConverter(BaseSignedNumericConverter[float]):  # noqa: D101
    _parse = staticmethod(float)


class SignedFloatConverter(BaseFloatConverter):  # noqa: D101
    regex: ClassVar[str] = r'-?[0-9]+(?:\.[0-9]+)?'


class PositiveFloatConverter(BaseFloatConverter):  # noqa: D101
    regex: ClassVar[str] = POSITIVE


class NegativeFloatConverter(BaseFloatConverter):  # noqa: D101
    regex: ClassVar[str] = f'-{POSITIVE}'


class NonNegativeFloatConverter(BaseFloatConverter):  # noqa: D101
    regex: ClassVar[str] = r'[0-9]+(?:\.[0-9]+)?'


class NonPositiveFloatConverter(BaseFloatConverter):  # noqa: D101
    regex: ClassVar[str] = f'{ZERO}|-{POSITIVE}'


class NonZeroFloatConverter(BaseFloatConverter):  # noqa: D101
    regex: ClassVar[str] = f'-?{POSITIVE}'
