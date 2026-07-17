import importlib
import warnings
from io import StringIO

from django.conf import settings
from django.core.management import call_command, get_commands
from django.test import override_settings

from django_boost.contrib.admin_tools.management.commands.adminsitelog import (
    Command as CanonicalCommand,
)
from django_boost.test import TestCase


def _deprecations(caught):
    return [w for w in caught if issubclass(w.category, DeprecationWarning)]


class TestAdminSiteLogLegacyAlias(TestCase):

    def test_legacy_command_subclasses_canonical(self):
        from django_boost.management.commands.adminsitelog import Command
        self.assertTrue(issubclass(Command, CanonicalCommand))

    def test_importing_legacy_module_does_not_warn(self):
        import django_boost.management.commands.adminsitelog as legacy
        self.addCleanup(importlib.reload, legacy)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            importlib.reload(legacy)
        self.assertEqual(_deprecations(caught), [])

    def test_running_command_does_not_warn_when_contrib_installed(self):
        # Default settings install django_boost.contrib.admin_tools, yet Django
        # resolves 'adminsitelog' to the core django_boost alias.
        self.addCleanup(get_commands.cache_clear)
        get_commands.cache_clear()
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            call_command('adminsitelog', stdout=StringIO(), stderr=StringIO())
        self.assertEqual(_deprecations(caught), [])

    def test_running_command_warns_when_contrib_not_installed(self):
        apps_without_contrib = [
            app for app in settings.INSTALLED_APPS
            if app != 'django_boost.contrib.admin_tools']
        self.addCleanup(get_commands.cache_clear)
        with override_settings(INSTALLED_APPS=apps_without_contrib):
            get_commands.cache_clear()
            with self.assertWarns(DeprecationWarning):
                call_command(
                    'adminsitelog', stdout=StringIO(), stderr=StringIO())

    def test_warning_tells_user_to_replace_not_add_the_app(self):
        # Both apps default their app_label to 'admin_tools' (neither
        # AppConfig sets an explicit label), so they cannot coexist in
        # INSTALLED_APPS; the message must say "replace", not "add".
        apps_without_contrib = [
            app for app in settings.INSTALLED_APPS
            if app != 'django_boost.contrib.admin_tools']
        self.addCleanup(get_commands.cache_clear)
        with override_settings(INSTALLED_APPS=apps_without_contrib):
            get_commands.cache_clear()
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                call_command(
                    'adminsitelog', stdout=StringIO(), stderr=StringIO())
        messages = [str(w.message) for w in _deprecations(caught)]
        self.assertTrue(any(
            "replace 'django_boost.admin_tools' with "
            "'django_boost.contrib.admin_tools'" in message
            for message in messages
        ), messages)
