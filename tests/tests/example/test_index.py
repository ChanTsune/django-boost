from django.test import TestCase
from django.urls import reverse


class TestIndexPage(TestCase):

    def test_renders_template_helper_playground(self):
        # A misused boost template helper in this page fails only at render
        # time, which the filters' own unit tests don't exercise.
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
