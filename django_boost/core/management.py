from django.core.management import base, ManagementUtility

from django_boost.core import get_version

__all__ = ["BaseCommand", "AppCommand"]


class CommandVersion:
    """Django-Boost command version."""

    def get_version(self):
        return get_version()


class BaseCommand(CommandVersion, base.BaseCommand):
    pass


class AppCommand(CommandVersion, base.AppCommand):
    pass


def execute_from_command_line(argv=None):
    """Run a ManagementUtility."""
    import os
    from django.conf import ENVIRONMENT_VARIABLE
    os.environ.setdefault(ENVIRONMENT_VARIABLE, 'django_boost.app.settings')
    utility = ManagementUtility(argv)
    utility.execute()
