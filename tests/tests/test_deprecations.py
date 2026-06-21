from django_boost.test import TestCase


class ZipFilterDeprecationTests(TestCase):
    def test_zip_filter_warns(self):
        from django_boost.templatetags.boost import _zip
        with self.assertWarns(DeprecationWarning):
            result = _zip([1, 2], [3, 4])
        self.assertEqual(list(result), [(1, 3), (2, 4)])


class JsonFieldDeprecationTests(TestCase):
    def test_jsonfield_init_warns(self):
        from django_boost.models.fields import JsonField
        with self.assertWarnsRegex(DeprecationWarning, r"Django 3\.1"):
            JsonField()
