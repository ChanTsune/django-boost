import os

from django.test import TestCase, override_settings
from django.urls import reverse

ROOT_PATH = os.path.dirname(__file__)


@override_settings(
    ROOT_URLCONF='django_boost.tests.urls_converters.urls',
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
            self.assertEqual(response.status_code, 200)
