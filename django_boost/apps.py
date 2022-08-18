"""This module provides django_boost application configuration."""

from django.apps import AppConfig
from django.core import checks

from django_boost.checks import check_database_router


class DjangoBoostConfig(AppConfig):
    """Class representing a Django-Boost and its configuration."""

    name = 'django_boost'
    verbose_name = 'Django Boost'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        checks.register(check_database_router, self.name)
