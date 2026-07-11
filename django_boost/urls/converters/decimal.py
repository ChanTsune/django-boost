"""Extensions for Django's ``django.urls`` path converters."""

from __future__ import annotations

import decimal
from typing import ClassVar

from django_boost.urls.converters._numeric import (
    BaseSignedNumericConverter, POSITIVE, ZERO)


class BaseDecimalConverter(BaseSignedNumericConverter[decimal.Decimal]):  # noqa: D101
    _parse = staticmethod(decimal.Decimal)


class SignedDecimalConverter(BaseDecimalConverter):  # noqa: D101
    regex: ClassVar[str] = r'-?[0-9]+(?:\.[0-9]+)?'


class PositiveDecimalConverter(BaseDecimalConverter):  # noqa: D101
    regex: ClassVar[str] = POSITIVE


class NegativeDecimalConverter(BaseDecimalConverter):  # noqa: D101
    regex: ClassVar[str] = f'-{POSITIVE}'


class NonNegativeDecimalConverter(BaseDecimalConverter):  # noqa: D101
    regex: ClassVar[str] = r'[0-9]+(?:\.[0-9]+)?'


class NonPositiveDecimalConverter(BaseDecimalConverter):  # noqa: D101
    regex: ClassVar[str] = f'{ZERO}|-{POSITIVE}'


class NonZeroDecimalConverter(BaseDecimalConverter):  # noqa: D101
    regex: ClassVar[str] = f'-?{POSITIVE}'
