import re

from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from django_boost.test import TestCase
from django_boost.urls.converters.float import (
    NegativeFloatConverter, NonNegativeFloatConverter,
    NonPositiveFloatConverter, NonZeroFloatConverter,
    PositiveFloatConverter, SignedFloatConverter)

from .base import ConverterTestCase

# (converter, predicate) — predicate(f) is True when str(f) must match the regex.
CONVERTERS = [
    (SignedFloatConverter, lambda f: True),
    (PositiveFloatConverter, lambda f: f > 0),
    (NegativeFloatConverter, lambda f: f < 0),
    (NonNegativeFloatConverter, lambda f: f >= 0),
    (NonPositiveFloatConverter, lambda f: f <= 0),
    (NonZeroFloatConverter, lambda f: f != 0),
]

# Canonical decimal literals only (no "-0"-style signed zero — see design doc).
DOMAIN_VALUES = [
    '0', '0.0', '0.00', '0.5', '-0.5', '5', '-5', '5.25', '-5.25',
    '007', '007.00', '-007', '007.5', '-007.5', '10.0', '-10.0', '10',
]


class TestFloatConversion(TestCase):

    def test_to_python_returns_float(self):
        self.assertEqual(SignedFloatConverter().to_python('-007.5'), -7.5)
        self.assertEqual(PositiveFloatConverter().to_python('007.5'), 7.5)
        self.assertEqual(NegativeFloatConverter().to_python('-5.5'), -5.5)
        self.assertEqual(NonNegativeFloatConverter().to_python('0'), 0.0)
        self.assertEqual(NonPositiveFloatConverter().to_python('-5'), -5.0)
        self.assertEqual(NonZeroFloatConverter().to_python('-5'), -5.0)

    def test_to_url_is_string(self):
        self.assertEqual(NegativeFloatConverter().to_url(-5.5), '-5.5')
        self.assertEqual(PositiveFloatConverter().to_url(7.25), '7.25')
        self.assertEqual(SignedFloatConverter().to_url(0.0), '0.0')


class TestFloatRegex(TestCase):

    def test_regex_matches_domain(self):
        for converter, predicate in CONVERTERS:
            fullmatch = re.compile(converter.regex).fullmatch
            for value in DOMAIN_VALUES:
                with self.subTest(converter=converter.__name__, value=value):
                    self.assertEqual(
                        bool(fullmatch(value)), predicate(float(value)))

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
            (PositiveFloatConverter, '007.5', True),
            (PositiveFloatConverter, '000.00', False),
            (NonZeroFloatConverter, '-007.5', True),
            (NonZeroFloatConverter, '-000.00', False),
            (NonNegativeFloatConverter, '000.00', True),
            (NegativeFloatConverter, '-000.00', False),
        ]
        for converter, value, expected in cases:
            fullmatch = re.compile(converter.regex).fullmatch
            with self.subTest(converter=converter.__name__, value=value):
                self.assertEqual(bool(fullmatch(value)), expected)


class TestFloatConverter(ConverterTestCase):

    def test_in_domain_values_route(self):
        case = [('signed_float', '5'), ('signed_float', '-5'),
                ('signed_float', '0'), ('signed_float', '5.25'),
                ('positive_float', '5'), ('positive_float', '0.5'),
                ('negative_float', '-5'), ('negative_float', '-0.5'),
                ('non_negative_float', '0'), ('non_negative_float', '5.5'),
                ('non_positive_float', '0'), ('non_positive_float', '-5.5'),
                ('non_zero_float', '5'), ('non_zero_float', '-5'),
                ('float', '5.5'), ('float', '0'),
                ]
        for name, value in case:
            with self.subTest(name=name, value=value):
                url = reverse(name, kwargs={name: value})
                self.assertStatusCodeEqual(self.client.get(url), 200)

    def test_out_of_domain_values_do_not_reverse(self):
        case = [('positive_float', '0'), ('positive_float', '0.00'),
                ('positive_float', '-5'),
                ('negative_float', '0'), ('negative_float', '5'),
                ('non_negative_float', '-5'),
                ('non_positive_float', '5'),
                ('non_zero_float', '0'), ('non_zero_float', '0.00'),
                ]
        for name, value in case:
            with self.subTest(name=name, value=value):
                with self.assertRaises(NoReverseMatch):
                    reverse(name, kwargs={name: value})

    def test_accepts_leading_zeros(self):
        for url in ['/positive_float/007.5', '/signed_float/-007.5',
                    '/non_zero_float/-007.5', '/non_negative_float/000.5']:
            with self.subTest(url=url):
                self.assertStatusCodeEqual(self.client.get(url), 200)

    def test_rejects_leading_zero_only(self):
        # '000.00' is zero, so it must not match the strictly-nonzero converters.
        for url in ['/positive_float/000.00', '/negative_float/-000.00',
                    '/non_zero_float/000.00']:
            with self.subTest(url=url):
                self.assertStatusCodeEqual(self.client.get(url), 404)

    def test_reverse_is_canonical(self):
        self.assertEqual(
            reverse('signed_float', kwargs={'signed_float': -5.5}),
            '/signed_float/-5.5')
        self.assertEqual(
            reverse('positive_float', kwargs={'positive_float': 7.25}),
            '/positive_float/7.25')
        self.assertEqual(
            reverse('non_positive_float', kwargs={'non_positive_float': 0.0}),
            '/non_positive_float/0.0')
