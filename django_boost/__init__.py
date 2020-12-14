import django
from django_boost.utils.version import get_version

VERSION = (1, 7, 2, 'final', 0)


__version__ = get_version()


if django.VERSION < (3, 2):
    default_app_config = 'django_boost.apps.DjangoBoostConfig'
