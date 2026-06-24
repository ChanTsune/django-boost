import importlib

from django_boost.contrib.admin_tools.management.commands.adminsitelog import (
    Command as CanonicalCommand,
)
from django_boost.test import TestCase


class TestAdminSiteLogLegacyAlias(TestCase):

    def test_legacy_command_reexports_canonical(self):
        from django_boost.management.commands.adminsitelog import Command
        self.assertIs(Command, CanonicalCommand)

    def test_importing_legacy_module_warns(self):
        import django_boost.management.commands.adminsitelog as legacy
        with self.assertWarns(DeprecationWarning):
            importlib.reload(legacy)
