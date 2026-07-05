from __future__ import annotations

import decimal
from typing import ClassVar

from django_boost.urls.converters._numeric import (
    BaseSignedNumericConverter, POSITIVE, ZERO)


class BaseDecimalConverter(BaseSignedNumericConverter[decimal.Decimal]):
    _parse = staticmethod(decimal.Decimal)


class SignedDecimalConverter(BaseDecimalConverter):
    regex: ClassVar[str] = r'-?[0-9]+(?:\.[0-9]+)?'


class PositiveDecimalConverter(BaseDecimalConverter):
    regex: ClassVar[str] = POSITIVE


class NegativeDecimalConverter(BaseDecimalConverter):
    regex: ClassVar[str] = f'-{POSITIVE}'


class NonNegativeDecimalConverter(BaseDecimalConverter):
    regex: ClassVar[str] = r'[0-9]+(?:\.[0-9]+)?'


class NonPositiveDecimalConverter(BaseDecimalConverter):
    regex: ClassVar[str] = f'{ZERO}|-{POSITIVE}'


class NonZeroDecimalConverter(BaseDecimalConverter):
    regex: ClassVar[str] = f'-?{POSITIVE}'
