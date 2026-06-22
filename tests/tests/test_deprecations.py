from django_boost.test import TestCase


class JsonFieldDeprecationTests(TestCase):
    def test_jsonfield_init_warns(self):
        from django_boost.models.fields import JsonField
        with self.assertWarnsRegex(DeprecationWarning, r"Django 3\.1"):
            JsonField()
