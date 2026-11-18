"""This module provides django_boost application configuration."""

from __future__ import annotations

from django.apps import AppConfig
from django.core import checks

from django_boost.checks import CHECKS


class DjangoBoostConfig(AppConfig):
    """Class representing a Django-Boost and its configuration."""

    name = 'django_boost'
    verbose_name = 'Django Boost'
    # Retain the historical AutoField default for pre-4.0 EmailUser migration
    # state, so adopters do not accidentally change the legacy table's PK type.
    default_auto_field = 'django.db.models.AutoField'

    def ready(self) -> None:
        """Register django_boost's system checks (``django_boost.checks.CHECKS``)."""
        for check in CHECKS:
            checks.register(check, self.name)
