"""This module provides django_boost application configuration."""

from __future__ import annotations

from django.apps import AppConfig
from django.core import checks

from django_boost.checks import CHECKS


class DjangoBoostConfig(AppConfig):
    """Class representing a Django-Boost and its configuration."""

    name = 'django_boost'
    verbose_name = 'Django Boost'
    # EmailUser shipped its migration with an AutoField primary key; keep the
    # auto field as AutoField so adopters are not forced into an INT->BIGINT
    # migration of the user table's primary key.
    default_auto_field = 'django.db.models.AutoField'

    def ready(self):
        """Register django_boost's system checks (``django_boost.checks.CHECKS``)."""
        for check in CHECKS:
            checks.register(check, self.name)
