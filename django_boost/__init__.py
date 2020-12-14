from django_boost.utils.version import get_version

VERSION = (1, 8, 0, 'alpha', 0)


__version__ = get_version()

default_app_config = 'django_boost.apps.DjangoBoostConfig'
