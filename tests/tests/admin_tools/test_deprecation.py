import django_boost.admin_tools
from django_boost.admin_tools.apps import AdminToolsConfig
from django_boost.admin_tools.management.commands.listsuperuser import (
    Command as LegacyCommand,
)
from django_boost.contrib.admin_tools.management.commands.listsuperuser import (
    Command as CanonicalCommand,
)
from django_boost.test import TestCase


class TestAdminToolsDeprecation(TestCase):

    def test_legacy_app_config_ready_warns(self):
        config = AdminToolsConfig(
            'django_boost.admin_tools', django_boost.admin_tools)
        with self.assertWarns(DeprecationWarning):
            config.ready()

    def test_legacy_command_reexports_canonical(self):
        self.assertIs(LegacyCommand, CanonicalCommand)
