"""App config for the deprecated ``django_boost.admin_tools`` app."""

from __future__ import annotations

import warnings

from django.apps import AppConfig


class AdminToolsConfig(AppConfig):
    """App config that warns on ``ready()`` that this app is a deprecated alias."""

    name = 'django_boost.admin_tools'

    def ready(self) -> None:  # noqa: D102
        warnings.warn(
            "'django_boost.admin_tools' is deprecated and will be removed in "
            "django-boost 4.0; use 'django_boost.contrib.admin_tools' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
