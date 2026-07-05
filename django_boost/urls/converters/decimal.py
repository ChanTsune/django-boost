from __future__ import annotations

import decimal
from typing import ClassVar

# branch 1: integer part has a non-zero digit (fraction optional)
# branch 2: integer part is all zeros, but the fraction has a non-zero digit
_POSITIVE = r'(?:[0-9]*[1-9][0-9]*(?:\.[0-9]+)?|0+\.[0-9]*[1-9][0-9]*)'
# the whole value is zero, e.g. 0, 00, 0.0, 0.00
_ZERO = r'0+(?:\.0+)?'


class BaseDecimalConverter:
    """Shared behavior for the signed-decimal path converters.

    Each subclass only declares ``regex``. Sign/zero classification looks
    at the whole value (integer part and fractional part together) rather
    than the integer part alone, so e.g. ``0.5`` counts as positive even
    though its integer part is ``0``. Parsing and reversing are common:
    the matched text is always a valid ``decimal.Decimal`` literal.
    """

    regex: ClassVar[str]

    def to_python(self, value: str) -> decimal.Decimal:
        return decimal.Decimal(value)

    def to_url(self, value: decimal.Decimal | str) -> str:
        return str(value)


class SignedDecimalConverter(BaseDecimalConverter):
    regex: ClassVar[str] = r'-?[0-9]+(?:\.[0-9]+)?'


class PositiveDecimalConverter(BaseDecimalConverter):
    regex: ClassVar[str] = _POSITIVE


class NegativeDecimalConverter(BaseDecimalConverter):
    regex: ClassVar[str] = f'-{_POSITIVE}'


class NonNegativeDecimalConverter(BaseDecimalConverter):
    regex: ClassVar[str] = r'[0-9]+(?:\.[0-9]+)?'


class NonPositiveDecimalConverter(BaseDecimalConverter):
    regex: ClassVar[str] = f'{_ZERO}|-{_POSITIVE}'


class NonZeroDecimalConverter(BaseDecimalConverter):
    regex: ClassVar[str] = f'-?{_POSITIVE}'
