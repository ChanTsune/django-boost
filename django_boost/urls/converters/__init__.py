"""Extensions for Django's ``django.urls`` path converters."""

from __future__ import annotations

from django.urls import register_converter

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

    regex = '[0-9a-fA-F]+'

    def to_url(self, value):
        if isinstance(value, int):
            return hex(value)[2:]
        return str(value)


class OctConverter:
    """Octal URL converter for non-negative integers.

    Negative values are not supported: ``reverse()`` with one raises
    ``NoReverseMatch``.
    """

    regex = '[0-7]+'

    def to_url(self, value):
        if isinstance(value, int):
            return oct(value)[2:]
        return str(value)


class BinConverter:
    """Binary URL converter for non-negative integers.

    Negative values are not supported: ``reverse()`` with one raises
    ``NoReverseMatch``.
    """

    regex = '[01]+'

    def to_url(self, value):
        if isinstance(value, int):
            return bin(value)[2:]
        return str(value)


class HexIntConverter(HexConverter):
    def to_python(self, value):
        return int(value, 16)


class OctIntConverter(OctConverter):
    def to_python(self, value):
        return int(value, 8)


class BinIntConverter(BinConverter):
    def to_python(self, value):
        return int(value, 2)


class HexStrConverter(HexConverter):
    def to_python(self, value):
        return value


class OctStrConverter(OctConverter):
    def to_python(self, value):
        return value


class BinStrConverter(BinConverter):
    def to_python(self, value):
        return value


BOOST_CONVERTERS = {
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
}


def register_boost_converters():
    """Register all of django_boost's URL converters (``BOOST_CONVERTERS``) with Django."""
    for name, klass in BOOST_CONVERTERS.items():
        register_converter(klass, name)
