import os

from django.test import override_settings
from django.urls import reverse
from django_boost.test import TestCase

ROOT_PATH = os.path.dirname(__file__)


@override_settings(
    ROOT_URLCONF='tests.tests.views.urls',
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(ROOT_PATH, 'templates')],
        'APP_DIRS': True,
    }],
)
class TestStringView(TestCase):

    def test_string_view(self):
        response = self.client.get(reverse('empty'))
        self.assertEqual(response.content, b'')

    def test_string_view_content(self):
        response = self.client.get(reverse('simple'))
        self.assertEqual(response.content, b'test string')

    def test_string_view_get_content(self):
        cases = [
            {'key1': 1, 'key2': 'one'}
        ]
        for e in cases:
            response = self.client.get(reverse('dynamic', kwargs=e))
            self.assertEqual(response.content, str(e).encode('utf-8'))

    def test_after_view_process(self):
        response = self.client.get(reverse('after'))
        self.assertEqual(response.content, b'processed')
        self.assertEqual(response["X-After-View-Process"], "yes")

    def test_after_view_process_on_short_circuit(self):
        # A mixin ahead of View in the MRO returns a 415 without calling
        # super().dispatch(); after_view_process must still run on it.
        response = self.client.get(reverse('after_short_circuit'))
        self.assertEqual(response.status_code, 415)
        self.assertEqual(response.get("X-After-View-Process"), "yes")

    def test_after_view_process_on_generic_view(self):
        # The hook fires through a generic view's full dispatch/render path.
        response = self.client.get(reverse('after_generic'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get("X-After-View-Process"), "yes")

    def test_after_view_process_on_head(self):
        response = self.client.head(reverse('after'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get("X-After-View-Process"), "yes")
