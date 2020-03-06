from django.apps import AppConfig
from django.core import checks

from django_boost.checks import check_database_router


class DjangoBoostConfig(AppConfig):
    name = 'django_boost'
    verbose_name = 'Django Boost'

    def ready(self):
        checks.register(check_database_router, self.name)
