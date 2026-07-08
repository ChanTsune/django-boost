"""Internal helpers used across django_boost; not part of the public API."""

from __future__ import annotations

from django_boost import __version__ as VERSION


def get_version() -> str:
    """Return django_boost's version string (``django_boost.__version__``)."""
    return VERSION


class Empty:
    """A class that does nothing to indicate an invalid value."""


EMPTY = Empty()


def is_empty(obj: object) -> bool:
    """Return `True` if `obj` is the `EMPTY` sentinel, `False` otherwise."""
    return isinstance(obj, Empty)
