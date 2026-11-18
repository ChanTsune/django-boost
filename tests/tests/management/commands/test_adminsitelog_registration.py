"""The adminsitelog command is available only from the optional admin-tools app."""

from importlib.util import find_spec

from django.conf import settings
from django.core.management import get_commands
from django.test import SimpleTestCase, override_settings


class AdminSiteLogRegistrationTests(SimpleTestCase):
    def tearDown(self):
        get_commands.cache_clear()
        super().tearDown()

    def test_core_alias_is_removed(self):
        self.assertIsNone(find_spec("django_boost.management.commands.adminsitelog"))

    def test_canonical_command_is_registered(self):
        get_commands.cache_clear()
        self.assertEqual(
            get_commands().get("adminsitelog"), "django_boost.contrib.admin_tools")

    def test_command_is_not_registered_without_contrib_app(self):
        installed_apps = [
            app for app in settings.INSTALLED_APPS
            if app != "django_boost.contrib.admin_tools"
        ]
        with override_settings(INSTALLED_APPS=installed_apps):
            get_commands.cache_clear()
            self.assertNotIn("adminsitelog", get_commands())
