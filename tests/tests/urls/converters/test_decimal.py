import decimal
import re

from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from django_boost.test import TestCase
from django_boost.urls.converters.decimal import (
    NegativeDecimalConverter, NonNegativeDecimalConverter,
    NonPositiveDecimalConverter, NonZeroDecimalConverter,
    PositiveDecimalConverter, SignedDecimalConverter)

from .base import ConverterTestCase

# (converter, predicate) — predicate(d) is True when str(d) must match the regex.
CONVERTERS = [
    (SignedDecimalConverter, lambda d: True),
    (PositiveDecimalConverter, lambda d: d > 0),
    (NegativeDecimalConverter, lambda d: d < 0),
    (NonNegativeDecimalConverter, lambda d: d >= 0),
    (NonPositiveDecimalConverter, lambda d: d <= 0),
    (NonZeroDecimalConverter, lambda d: d != 0),
]

# Canonical decimal literals only (no "-0"-style signed zero — see design doc).
DOMAIN_VALUES = [
    '0', '0.0', '0.00', '0.5', '-0.5', '5', '-5', '5.25', '-5.25',
    '007', '007.00', '-007', '007.5', '-007.5', '10.0', '-10.0', '10',
]


class TestDecimalConversion(TestCase):

    def test_to_python_returns_decimal(self):
        self.assertEqual(
            SignedDecimalConverter().to_python('-007.5'),
            decimal.Decimal('-7.5'))
        self.assertEqual(
            PositiveDecimalConverter().to_python('007.5'),
            decimal.Decimal('7.5'))
        self.assertEqual(
            NegativeDecimalConverter().to_python('-5.5'),
            decimal.Decimal('-5.5'))
        self.assertEqual(
            NonNegativeDecimalConverter().to_python('0'), decimal.Decimal('0'))
        self.assertEqual(
            NonPositiveDecimalConverter().to_python('-5'), decimal.Decimal('-5'))
        self.assertEqual(
            NonZeroDecimalConverter().to_python('-5'), decimal.Decimal('-5'))

    def test_to_url_is_string(self):
        self.assertEqual(
            NegativeDecimalConverter().to_url(decimal.Decimal('-5.5')), '-5.5')
        self.assertEqual(
            PositiveDecimalConverter().to_url(decimal.Decimal('7.25')), '7.25')
        self.assertEqual(
            SignedDecimalConverter().to_url(decimal.Decimal('0')), '0')


class TestDecimalRegex(TestCase):

    def test_regex_matches_domain(self):
        for converter, predicate in CONVERTERS:
            fullmatch = re.compile(converter.regex).fullmatch
            for value in DOMAIN_VALUES:
                with self.subTest(converter=converter.__name__, value=value):
                    self.assertEqual(
                        bool(fullmatch(value)),
                        predicate(decimal.Decimal(value)))

    def test_regex_rejects_leading_plus(self):
        for converter, _ in CONVERTERS:
            fullmatch = re.compile(converter.regex).fullmatch
            with self.subTest(converter=converter.__name__):
                self.assertIsNone(fullmatch('+5'))

    def test_regex_rejects_trailing_dot(self):
        for converter, _ in CONVERTERS:
            fullmatch = re.compile(converter.regex).fullmatch
            with self.subTest(converter=converter.__name__):
                self.assertIsNone(fullmatch('5.'))

    def test_regex_leading_zeros(self):
        cases = [
            (PositiveDecimalConverter, '007.5', True),
            (PositiveDecimalConverter, '000.00', False),
            (NonZeroDecimalConverter, '-007.5', True),
            (NonZeroDecimalConverter, '-000.00', False),
            (NonNegativeDecimalConverter, '000.00', True),
            (NegativeDecimalConverter, '-000.00', False),
        ]
        for converter, value, expected in cases:
            fullmatch = re.compile(converter.regex).fullmatch
            with self.subTest(converter=converter.__name__, value=value):
                self.assertEqual(bool(fullmatch(value)), expected)


class TestDecimalConverter(ConverterTestCase):

    def test_in_domain_values_route(self):
        case = [('signed_decimal', '5'), ('signed_decimal', '-5'),
                ('signed_decimal', '0'), ('signed_decimal', '5.25'),
                ('positive_decimal', '5'), ('positive_decimal', '0.5'),
                ('negative_decimal', '-5'), ('negative_decimal', '-0.5'),
                ('non_negative_decimal', '0'), ('non_negative_decimal', '5.5'),
                ('non_positive_decimal', '0'), ('non_positive_decimal', '-5.5'),
                ('non_zero_decimal', '5'), ('non_zero_decimal', '-5'),
                ('decimal', '5.5'), ('decimal', '0'),
                ]
        for name, value in case:
            with self.subTest(name=name, value=value):
                url = reverse(name, kwargs={name: value})
                self.assertStatusCodeEqual(self.client.get(url), 200)

    def test_out_of_domain_values_do_not_reverse(self):
        case = [('positive_decimal', '0'), ('positive_decimal', '0.00'),
                ('positive_decimal', '-5'),
                ('negative_decimal', '0'), ('negative_decimal', '5'),
                ('non_negative_decimal', '-5'),
                ('non_positive_decimal', '5'),
                ('non_zero_decimal', '0'), ('non_zero_decimal', '0.00'),
                ]
        for name, value in case:
            with self.subTest(name=name, value=value):
                with self.assertRaises(NoReverseMatch):
                    reverse(name, kwargs={name: value})

    def test_accepts_leading_zeros(self):
        for url in ['/positive_decimal/007.5', '/signed_decimal/-007.5',
                    '/non_zero_decimal/-007.5', '/non_negative_decimal/000.5']:
            with self.subTest(url=url):
                self.assertStatusCodeEqual(self.client.get(url), 200)

    def test_rejects_leading_zero_only(self):
        # '000.00' is zero, so it must not match the strictly-nonzero converters.
        for url in ['/positive_decimal/000.00', '/negative_decimal/-000.00',
                    '/non_zero_decimal/000.00']:
            with self.subTest(url=url):
                self.assertStatusCodeEqual(self.client.get(url), 404)

    def test_reverse_is_canonical(self):
        self.assertEqual(
            reverse('signed_decimal',
                    kwargs={'signed_decimal': decimal.Decimal('-5.5')}),
            '/signed_decimal/-5.5')
        self.assertEqual(
            reverse('positive_decimal',
                    kwargs={'positive_decimal': decimal.Decimal('7.25')}),
            '/positive_decimal/7.25')
        self.assertEqual(
            reverse('non_positive_decimal',
                    kwargs={'non_positive_decimal': decimal.Decimal('0')}),
            '/non_positive_decimal/0')
