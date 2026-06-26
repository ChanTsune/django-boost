from __future__ import annotations

from typing import Any

from django_boost.core import EMPTY, is_empty


def getattrs(obj: object, *names: str, default: Any = EMPTY) -> tuple[Any, ...]:
    """Get multiple attributes."""
    if is_empty(default):
        return tuple(getattr(obj, name) for name in names)
    return tuple(getattr(obj, name, default) for name in names)


def getattr_chain(obj: object, name: str, default: Any = EMPTY) -> Any:
    """
    Get attribute.

    example ::

    getattr_chain(obj, '__class__.__name__')
    getattr_chain(obj, '__class__.__name__', default_value)
    """
    try:
        for n in name.split('.'):
            obj = getattr(obj, n)
        return obj
    except AttributeError as e:
        if is_empty(default):
            raise AttributeError('%s has no Attribute %s' % (obj, name)) from e
        return default


def hasattrs(obj: object, *names: str) -> bool:
    """Check if obj has all attribute names given in the argument."""
    try:
        getattrs(obj, *names)
        return True
    except AttributeError:
        return False


def hasattr_chain(obj: object, name: str) -> bool:
    """
    Check if obj have an attribute named.

    example ::

    hasattr_chain(obj, '__class__.__name__')
    """
    try:
        for n in name.split('.'):
            obj = getattr(obj, n)
        return True
    except AttributeError:
        return False
