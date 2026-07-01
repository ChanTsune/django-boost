import re

from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from django_boost.test import TestCase
from django_boost.urls.converters.integer import (
    NegativeIntConverter, NonNegativeIntConverter, NonPositiveIntConverter,
    NonZeroIntConverter, PositiveIntConverter, SignedIntConverter)

from .base import ConverterTestCase

# (converter, predicate) — predicate(i) is True when str(i) must match the regex.
CONVERTERS = [
    (SignedIntConverter, lambda i: True),
    (PositiveIntConverter, lambda i: i > 0),
    (NegativeIntConverter, lambda i: i < 0),
    (NonNegativeIntConverter, lambda i: i >= 0),
    (NonPositiveIntConverter, lambda i: i <= 0),
    (NonZeroIntConverter, lambda i: i != 0),
]


class TestIntegerConverter(ConverterTestCase):

    def test_in_domain_values_route(self):
        case = [('signed_int', 5), ('signed_int', -5), ('signed_int', 0),
                ('positive_int', 5), ('positive_int', 1),
                ('negative_int', -5), ('negative_int', -1),
                ('non_negative_int', 0), ('non_negative_int', 5),
                ('non_positive_int', 0), ('non_positive_int', -5),
                ('non_zero_int', 5), ('non_zero_int', -5),
                ]
        for name, value in case:
            with self.subTest(name=name, value=value):
                url = reverse(name, kwargs={name: value})
                self.assertStatusCodeEqual(self.client.get(url), 200)

    def test_out_of_domain_values_do_not_reverse(self):
        case = [('positive_int', 0), ('positive_int', -5),
                ('negative_int', 0), ('negative_int', 5),
                ('non_negative_int', -5),
                ('non_positive_int', 5),
                ('non_zero_int', 0),
                ]
        for name, value in case:
            with self.subTest(name=name, value=value):
                with self.assertRaises(NoReverseMatch):
                    reverse(name, kwargs={name: value})

    def test_accepts_leading_zeros(self):
        for url in ['/positive_int/007', '/signed_int/-007',
                    '/non_zero_int/-007', '/non_negative_int/000']:
            with self.subTest(url=url):
                self.assertStatusCodeEqual(self.client.get(url), 200)

    def test_rejects_leading_zero_only(self):
        # '000' is zero, so it must not match the strictly-nonzero converters.
        for url in ['/positive_int/000', '/negative_int/-000',
                    '/non_zero_int/000']:
            with self.subTest(url=url):
                self.assertStatusCodeEqual(self.client.get(url), 404)

    def test_reverse_is_canonical(self):
        self.assertEqual(
            reverse('signed_int', kwargs={'signed_int': -5}), '/signed_int/-5')
        self.assertEqual(
            reverse('positive_int', kwargs={'positive_int': 7}),
            '/positive_int/7')
        self.assertEqual(
            reverse('non_positive_int', kwargs={'non_positive_int': 0}),
            '/non_positive_int/0')


class TestIntegerConversion(TestCase):

    def test_to_python_returns_int(self):
        self.assertEqual(SignedIntConverter().to_python('-007'), -7)
        self.assertEqual(PositiveIntConverter().to_python('007'), 7)
        self.assertEqual(NegativeIntConverter().to_python('-5'), -5)
        self.assertEqual(NonNegativeIntConverter().to_python('0'), 0)
        self.assertEqual(NonPositiveIntConverter().to_python('-5'), -5)
        self.assertEqual(NonZeroIntConverter().to_python('-5'), -5)

    def test_to_url_is_string(self):
        self.assertEqual(NegativeIntConverter().to_url(-5), '-5')
        self.assertEqual(PositiveIntConverter().to_url(7), '7')
        self.assertEqual(SignedIntConverter().to_url(0), '0')


class TestIntegerRegex(TestCase):

    def test_regex_matches_domain(self):
        for converter, predicate in CONVERTERS:
            fullmatch = re.compile(converter.regex).fullmatch
            for i in range(-50, 51):
                with self.subTest(converter=converter.__name__, i=i):
                    self.assertEqual(bool(fullmatch(str(i))), predicate(i))

    def test_regex_rejects_leading_plus(self):
        for converter, _ in CONVERTERS:
            fullmatch = re.compile(converter.regex).fullmatch
            with self.subTest(converter=converter.__name__):
                self.assertIsNone(fullmatch('+5'))

    def test_regex_leading_zeros(self):
        cases = [
            (PositiveIntConverter, '007', True),
            (PositiveIntConverter, '000', False),
            (NonZeroIntConverter, '-007', True),
            (NonZeroIntConverter, '-000', False),
            (NonNegativeIntConverter, '000', True),
            (NegativeIntConverter, '-000', False),
        ]
        for converter, value, expected in cases:
            fullmatch = re.compile(converter.regex).fullmatch
            with self.subTest(converter=converter.__name__, value=value):
                self.assertEqual(bool(fullmatch(value)), expected)
