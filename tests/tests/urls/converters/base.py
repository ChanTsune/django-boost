import os

from django.test import override_settings

from django_boost.test import TestCase

ROOT_PATH = os.path.dirname(__file__)


@override_settings(
    ROOT_URLCONF='tests.tests.urls.converters.urls',
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
class ConverterTestCase(TestCase):
    """Route requests through the boost converter URLConf for these tests."""
