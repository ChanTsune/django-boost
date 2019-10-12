from django_boost import __version__ as VERSION


def get_version():
    return VERSION


class Empty:
    """A class that does nothing to indicate an invalid value."""


EMPTY = Empty()


def is_empty(obj):
    return isinstance(obj, Empty)
