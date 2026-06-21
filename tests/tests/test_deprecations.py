from django.core.management import call_command

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


class SupportHerokuDeprecationTests(TestCase):
    def test_support_heroku_warns(self):
        with self.assertWarnsRegex(DeprecationWarning, r"support_heroku.*django-boost 3\.0"):
            call_command("support_heroku")

    @classmethod
    def tearDownClass(cls):
        import os
        from django.conf import settings

        for name in ["Procfile", "runtime.txt", "requirements.txt"]:
            fp = os.path.join(settings.BASE_DIR, name)
            if os.path.exists(fp):
                os.remove(fp)
        super().tearDownClass()
