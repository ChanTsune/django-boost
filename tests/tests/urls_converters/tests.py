import os

from django.test import override_settings
from django.urls import reverse

from django_boost.test import TestCase

ROOT_PATH = os.path.dirname(__file__)


@override_settings(
    ROOT_URLCONF='tests.tests.urls_converters.urls',
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(ROOT_PATH, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django_boost.context_processors.user_agent',
            ],
        },
    }]
)
class TestConverter(TestCase):

    def test_path_converters(self):
        case = [('bin', '1010'),
                ('bin', 12),
                ('oct', '7'),
                ('oct', 7),
                ('hex', 'd'),
                ('hex', 12),
                ('bin_str', '1010'),
                ('oct_str', '236'),
                ('hex_str', '234'),
                ('float', 1.1),
                ('float', '1.1'),
                ('float', 1),
                ('float', '1'),
                ('date', '2020/2/29'),
                ]
        for name, value in case:
            url = reverse(name, kwargs={name: value})
            response = self.client.get(url)
            self.assertStatusCodeEqual(response, 200)

    def test_failed_case(self):
        from django.urls.exceptions import NoReverseMatch

        with self.assertRaises(NoReverseMatch):
            reverse('float', kwargs={'float': '1.'})

        with self.assertRaises(NoReverseMatch):
            reverse('date', kwargs={'date': '2019/2/29'})


class TestRegex(TestCase):

    DATE_FORMAT = "%d/%d"

    DATE_TEST_CASE = [(m, d) for m in range(20) for d in range(40)]

    def test_year_regex(self):
        import re
        from calendar import isleap as _isleep
        from django_boost.urls.converters.date import REGEX_LEAP_YEAR

        regex_is_leap = re.compile(REGEX_LEAP_YEAR).fullmatch

        def isleap(value):
            return value != 0 and _isleep(value)

        for i in range(10000):
            value = str(i)
            with self.subTest(value, value=value):
                result = bool(regex_is_leap(value))
                self.assertEqual(isleap(i), result)

    def test_date_31_regex(self):
        import re
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
        import re
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
        import re
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
        import re
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
        import re
        from datetime import datetime
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
