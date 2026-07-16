"""Extensions for Django's ``django.urls`` path converters."""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING, cast

from django.urls import register_converter

if TYPE_CHECKING:
    from django.urls.converters import _Converter

from django_boost.urls.converters.date import DateConverter
from django_boost.urls.converters.decimal import (
    NegativeDecimalConverter, NonNegativeDecimalConverter,
    NonPositiveDecimalConverter, NonZeroDecimalConverter,
    PositiveDecimalConverter, SignedDecimalConverter)
from django_boost.urls.converters.float import (
    NegativeFloatConverter, NonNegativeFloatConverter,
    NonPositiveFloatConverter, NonZeroFloatConverter,
    PositiveFloatConverter, SignedFloatConverter)
from django_boost.urls.converters.integer import (
    NegativeIntConverter, NonNegativeIntConverter, NonPositiveIntConverter,
    NonZeroIntConverter, PositiveIntConverter, SignedIntConverter)


class HexConverter:
    """Hexadecimal URL converter for non-negative integers.

    Negative values are not supported: ``reverse()`` with one raises
    ``NoReverseMatch``.
    """

    regex: ClassVar[str] = '[0-9a-fA-F]+'

    def to_url(self, value: int | str) -> str:  # noqa: D102
        if isinstance(value, int):
            return hex(value)[2:]
        return str(value)


class OctConverter:
    """Octal URL converter for non-negative integers.

    Negative values are not supported: ``reverse()`` with one raises
    ``NoReverseMatch``.
    """

    regex: ClassVar[str] = '[0-7]+'

    def to_url(self, value: int | str) -> str:  # noqa: D102
        if isinstance(value, int):
            return oct(value)[2:]
        return str(value)


class BinConverter:
    """Binary URL converter for non-negative integers.

    Negative values are not supported: ``reverse()`` with one raises
    ``NoReverseMatch``.
    """

    regex: ClassVar[str] = '[01]+'

    def to_url(self, value: int | str) -> str:  # noqa: D102
        if isinstance(value, int):
            return bin(value)[2:]
        return str(value)


class HexIntConverter(HexConverter):  # noqa: D101
    def to_python(self, value: str) -> int:  # noqa: D102
        return int(value, 16)


class OctIntConverter(OctConverter):  # noqa: D101
    def to_python(self, value: str) -> int:  # noqa: D102
        return int(value, 8)


class BinIntConverter(BinConverter):  # noqa: D101
    def to_python(self, value: str) -> int:  # noqa: D102
        return int(value, 2)


class HexStrConverter(HexConverter):  # noqa: D101
    def to_python(self, value: str) -> str:  # noqa: D102
        return value


class OctStrConverter(OctConverter):  # noqa: D101
    def to_python(self, value: str) -> str:  # noqa: D102
        return value


class BinStrConverter(BinConverter):  # noqa: D101
    def to_python(self, value: str) -> str:  # noqa: D102
        return value


# The converters mix ClassVar[str] regex (this package's local convention,
# e.g. integer.py) with plain-str regex; mypy's type[X] <: type[_Converter]
# check only recognizes the latter, so the heterogeneous mapping needs one
# cast to assert what's structurally already true.
BOOST_CONVERTERS = cast("dict[str, type[_Converter]]", {
    'bin': BinIntConverter,
    'oct': OctIntConverter,
    'hex': HexIntConverter,
    'bin_str': BinStrConverter,
    'oct_str': OctStrConverter,
    'hex_str': HexStrConverter,
    'float': NonNegativeFloatConverter,
    'signed_float': SignedFloatConverter,
    'positive_float': PositiveFloatConverter,
    'negative_float': NegativeFloatConverter,
    'non_negative_float': NonNegativeFloatConverter,
    'non_positive_float': NonPositiveFloatConverter,
    'non_zero_float': NonZeroFloatConverter,
    'date': DateConverter,
    'signed_int': SignedIntConverter,
    'positive_int': PositiveIntConverter,
    'negative_int': NegativeIntConverter,
    'non_negative_int': NonNegativeIntConverter,
    'non_positive_int': NonPositiveIntConverter,
    'non_zero_int': NonZeroIntConverter,
    'decimal': NonNegativeDecimalConverter,
    'signed_decimal': SignedDecimalConverter,
    'positive_decimal': PositiveDecimalConverter,
    'negative_decimal': NegativeDecimalConverter,
    'non_negative_decimal': NonNegativeDecimalConverter,
    'non_positive_decimal': NonPositiveDecimalConverter,
    'non_zero_decimal': NonZeroDecimalConverter,
})


def register_boost_converters() -> None:
    """Register all of django_boost's URL converters (``BOOST_CONVERTERS``) with Django."""
    for name, klass in BOOST_CONVERTERS.items():
        register_converter(klass, name)
