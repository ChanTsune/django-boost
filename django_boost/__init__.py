from django_boost.utils.version import get_version

VERSION = (2, 0, 0, 'final', 0)


__version__ = get_version()

try:
    import django
    if django.VERSION < (3, 2):
        default_app_config = 'django_boost.apps.DjangoBoostConfig'
except ImportError: # noqa
    pass  # noqa
