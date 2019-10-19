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

    def test_a(self):
        case = [('bin', '1010'),
                ('bin', 12),
                ('oct', '7'),
                ('oct', 7),
                ('hex', 'd'),
                ('hex', 12),
                ('bin_str', '1010'),
                ('oct_str', '236'),
                ('hex_str', '234')]
        for name, value in case:
            url = reverse(name, kwargs={name: value})
            response = self.client.get(url)
            self.assertStatusCodeEqual(response, 200)


class TestRegex(TestCase):

    def test_year_regex(self):
        import re
        from calendar import isleap
        from django_boost.urls.converters.date import REGEX_LEAP_YEAR

        regex_leap_year = re.compile(REGEX_LEAP_YEAR)

        for i in range(1, 10001):
            value = str(i)
            with self.subTest(value, value=value):
                result = bool(regex_leap_year.fullmatch(value))
                self.assertEqual(isleap(i), result)
