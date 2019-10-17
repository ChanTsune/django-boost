from django.core.management import base

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
