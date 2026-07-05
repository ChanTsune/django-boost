from __future__ import annotations

from collections.abc import Collection, Iterable, Iterator
from typing import TypeVar

__all__ = ["loopfirst", "loopfirstlast", "looplast"]

_T = TypeVar("_T")


def loopfirst(iterable: Iterable[_T]) -> Iterator[tuple[bool, _T]]:
    """
    Loop util.

    Yield True when the first element of the given iterator object,
    False otherwise.
    """
    it = iter(iterable)
    for i, val in enumerate(it):
        yield i == 0, val


def looplast(iterable: Iterable[_T]) -> Iterator[tuple[bool, _T]]:
    """
    Loop util.

    Yield True when the last element of the given iterator object,
    False otherwise.
    """
    items: Collection[_T] = (
        iterable if isinstance(iterable, Collection) else list(iterable))
    last_index = len(items) - 1
    for i, val in enumerate(items):
        yield i == last_index, val


def loopfirstlast(iterable: Iterable[_T]) -> Iterator[tuple[bool, _T]]:
    """
    Combine `loopfirst` and `looplast`.

    Yield True if the first and last element of the iterator object,
    False otherwise.
    """
    items: Collection[_T] = (
        iterable if isinstance(iterable, Collection) else list(iterable))
    last_index = len(items) - 1
    for i, val in enumerate(items):
        yield i == 0 or i == last_index, val
