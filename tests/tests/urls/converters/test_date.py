import re
from calendar import isleap as _isleap
from datetime import date, datetime

from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from django_boost.test import TestCase

from .base import ConverterTestCase


class TestDateConverter(ConverterTestCase):

    def test_matches_leap_day(self):
        url = reverse('date', kwargs={'date': '2020/2/29'})
        self.assertStatusCodeEqual(self.client.get(url), 200)

    def test_rejects_invalid_leap_day(self):
        with self.assertRaises(NoReverseMatch):
            reverse('date', kwargs={'date': '2019/2/29'})

    def test_accepts_zero_padded(self):
        response = self.client.get('/date/2020/02/29')
        self.assertStatusCodeEqual(response, 200)

    def test_reverses_datetime(self):
        url = reverse('date', kwargs={'date': datetime(2020, 1, 5)})
        self.assertEqual(url, '/date/2020/1/5')
        self.assertStatusCodeEqual(self.client.get(url), 200)

    def test_accepts_short_year(self):
        response = self.client.get('/date/48/2/29')
        self.assertStatusCodeEqual(response, 200)

    def test_reverses_short_year_datetime(self):
        url = reverse('date', kwargs={'date': datetime(48, 2, 29)})
        self.assertEqual(url, '/date/48/2/29')
        self.assertStatusCodeEqual(self.client.get(url), 200)

    def test_reverses_date(self):
        url = reverse('date', kwargs={'date': date(2020, 1, 5)})
        self.assertEqual(url, '/date/2020/1/5')
        self.assertStatusCodeEqual(self.client.get(url), 200)


class TestRegex(TestCase):

    DATE_FORMAT = "%d/%d"

    DATE_TEST_CASE = [(m, d) for m in range(20) for d in range(40)]

    def test_year_regex(self):
        from django_boost.urls.converters.date import REGEX_LEAP_YEAR

        regex_is_leap = re.compile(REGEX_LEAP_YEAR).fullmatch

        def isleap(value):
            return value != 0 and _isleap(value)

        for i in range(10000):
            value = str(i)
            with self.subTest(value, value=value):
                result = bool(regex_is_leap(value))
                self.assertEqual(isleap(i), result)

    def test_date_31_regex(self):
        from django_boost.urls.converters.date import REGEX_DATE_31

        regex_date_31_fullmatch = re.compile(REGEX_DATE_31).fullmatch

        for m, d in self.DATE_TEST_CASE:
            value = self.DATE_FORMAT % (m, d)
            with self.subTest(value, value=value):
                result = bool(regex_date_31_fullmatch(value))
                if m in [1, 3, 5, 7, 8, 10, 12] and d in range(1, 32):
                    self.assertTrue(result)
                else:
                    self.assertFalse(result)

    def test_date_30_regex(self):
        from django_boost.urls.converters.date import REGEX_DATE_30

        regex_date_30_fullmatch = re.compile(REGEX_DATE_30).fullmatch

        for m, d in self.DATE_TEST_CASE:
            value = self.DATE_FORMAT % (m, d)
            with self.subTest(value, value=value):
                result = bool(regex_date_30_fullmatch(value))
                if m in [4, 6, 9, 11] and d in range(1, 31):
                    self.assertTrue(result)
                else:
                    self.assertFalse(result)

    def test_date_29_regex(self):
        from django_boost.urls.converters.date import REGEX_DATE_29

        regex_date_29_fullmatch = re.compile(REGEX_DATE_29).fullmatch

        for m, d in self.DATE_TEST_CASE:
            value = self.DATE_FORMAT % (m, d)
            with self.subTest(value, value=value):
                result = bool(regex_date_29_fullmatch(value))
                if m == 2 and d in range(1, 30):
                    self.assertTrue(result)
                else:
                    self.assertFalse(result)

    def test_date_28_regex(self):
        from django_boost.urls.converters.date import REGEX_DATE_28

        regex_date_28_fullmatch = re.compile(REGEX_DATE_28).fullmatch

        for m, d in self.DATE_TEST_CASE:
            value = self.DATE_FORMAT % (m, d)
            with self.subTest(value, value=value):
                result = bool(regex_date_28_fullmatch(value))
                if m == 2 and d in range(1, 29):
                    self.assertTrue(result)
                else:
                    self.assertFalse(result)

    def test_date_time_regex(self):
        from django_boost.urls.converters.date import REGEX_DATE

        regex_fullmatch = re.compile(REGEX_DATE).fullmatch

        def is_valid_date(y, m, d):
            try:
                datetime(year=y, month=m, day=d)
                return True
            except ValueError:
                return False

        for y in range(10000):
            for m in range(14):
                for d in range(32):
                    with self.subTest("%s/%s/%s" % (y, m, d)):
                        self.assertEqual(is_valid_date(y, m, d), bool(
                            regex_fullmatch("%s/%s/%s" % (y, m, d))))
