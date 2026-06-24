"""This module provides django_boost application configuration."""

from __future__ import annotations

from django.apps import AppConfig
from django.core import checks

from django_boost.checks import CHECKS


class DjangoBoostConfig(AppConfig):
    """Class representing a Django-Boost and its configuration."""

    name = 'django_boost'
    verbose_name = 'Django Boost'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        for check in CHECKS:
            checks.register(check, self.name)
