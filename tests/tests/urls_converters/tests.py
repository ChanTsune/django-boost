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
                ]
        for name, value in case:
            url = reverse(name, kwargs={name: value})
            response = self.client.get(url)
            self.assertStatusCodeEqual(response, 200)

    def test_failed_case(self):
        from django.urls.exceptions import NoReverseMatch

        with self.assertRaises(NoReverseMatch):
            reverse('float', kwargs={'float': '1.'})
