from django.test import TestCase as DjangoTestCase


class TestCase(DjangoTestCase):

    def assertStatusCodeEqual(self, response, code):
        self.assertEqual(response.status_code, code)

    def assertStatusCodeNotEqual(self, response, code):
        self.assertNotEqual(response.status_code, code)

    def assertStatusCodeIn(self, response, codes):
        self.assertIn(response.status_code, codes)
