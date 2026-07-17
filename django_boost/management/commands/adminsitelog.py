"""Deprecated ``django_boost`` alias for ``contrib.admin_tools``'s ``adminsitelog`` command."""

from __future__ import annotations

import warnings
from typing import Any

from django.apps import apps

from django_boost.contrib.admin_tools.management.commands.adminsitelog import (
    Command as _Command,
)

__all__ = ['Command']

ADMIN_TOOLS_APP = "django_boost.contrib.admin_tools"


class Command(_Command):
    """Deprecated ``django_boost`` alias for the ``contrib.admin_tools`` command.

    Django resolves ``adminsitelog`` to this core ``django_boost`` alias even
    when ``django_boost.contrib.admin_tools`` is installed, because the core
    app precedes it in ``INSTALLED_APPS``. The deprecation warning is therefore
    emitted at run time only when that app is absent -- i.e. only for projects
    that have not migrated -- so correctly configured projects are not warned.
    """

    def execute(self, *args: Any, **options: Any) -> str | None:  # noqa: D102
        if not apps.is_installed(ADMIN_TOOLS_APP):
            warnings.warn(
                "Running 'adminsitelog' from 'django_boost' is deprecated; "
                "replace 'django_boost.admin_tools' with "
                "'django_boost.contrib.admin_tools' in INSTALLED_APPS. The "
                "'django_boost' command alias will be removed in "
                "django-boost 4.0.",
                DeprecationWarning,
                stacklevel=2,
            )
        return super().execute(*args, **options)
