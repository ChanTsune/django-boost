from __future__ import annotations

from typing import ClassVar

from django_boost.urls.converters._numeric import (
    BaseSignedNumericConverter, POSITIVE, ZERO)


class BaseFloatConverter(BaseSignedNumericConverter[float]):
    _parse = staticmethod(float)


class SignedFloatConverter(BaseFloatConverter):
    regex: ClassVar[str] = r'-?[0-9]+(?:\.[0-9]+)?'


class PositiveFloatConverter(BaseFloatConverter):
    regex: ClassVar[str] = POSITIVE


class NegativeFloatConverter(BaseFloatConverter):
    regex: ClassVar[str] = f'-{POSITIVE}'


class NonNegativeFloatConverter(BaseFloatConverter):
    regex: ClassVar[str] = r'[0-9]+(?:\.[0-9]+)?'


class NonPositiveFloatConverter(BaseFloatConverter):
    regex: ClassVar[str] = f'{ZERO}|-{POSITIVE}'


class NonZeroFloatConverter(BaseFloatConverter):
    regex: ClassVar[str] = f'-?{POSITIVE}'
