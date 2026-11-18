"""Only the canonical admin-tools app remains importable in 4.0."""

from importlib.util import find_spec

from django.apps import apps
from django.test import SimpleTestCase


class CanonicalAdminToolsAppTests(SimpleTestCase):
    def test_deprecated_app_path_is_removed(self):
        self.assertIsNone(find_spec("django_boost.admin_tools"))

    def test_canonical_app_is_installed(self):
        self.assertEqual(
            apps.get_app_config("admin_tools").name,
            "django_boost.contrib.admin_tools",
        )
