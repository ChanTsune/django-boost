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

    Without a default, the underlying ``AttributeError`` propagates unchanged,
    so a descriptor that raises an ``AttributeError`` subclass (e.g. a reverse
    one-to-one accessor) keeps its type and message. With a default, any
    ``AttributeError`` yields the default, like the builtin ``getattr``.
    """
    try:
        for n in name.split('.'):
            obj = getattr(obj, n)
        return obj
    except AttributeError:
        if is_empty(default):
            raise
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

    Like the builtin ``hasattr``, this returns ``False`` when accessing any
    segment raises ``AttributeError`` (including subclasses raised inside a
    descriptor), so it cannot tell a missing attribute from a raising one.
    """
    try:
        for n in name.split('.'):
            obj = getattr(obj, n)
        return True
    except AttributeError:
        return False
