from django.test import override_settings
from django.urls import reverse
from django_boost.test import TestCase


@override_settings(
    ROOT_URLCONF='tests.tests.views.urls',
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
