VERSION = (1, 4, 1)

def get_version(version=VERSION):
    if version[2] == 0:
        return "%s.%s" % version[:2]
    return "%s.%s.%s" % version

__version__ = get_version()

default_app_config = 'django_boost.apps.DjangoBoostConfig'
