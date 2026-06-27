from __future__ import annotations

from collections.abc import Iterable, Iterator, Sequence
from typing import TypeVar

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


def looplast(iterable: Sequence[_T]) -> Iterator[tuple[bool, _T]]:
    """
    Loop util.

    Yield True when the last element of the given iterator object,
    False otherwise.
    """
    it = iterable
    last_index = len(it) - 1
    for i, val in enumerate(it):
        yield i == last_index, val


def loopfirstlast(iterable: Sequence[_T]) -> Iterator[tuple[bool, _T]]:
    """
    A function combining `firstloop` and` lastloop`.

    Yield True if the first and last element of the iterator object,
    False otherwise.
    """
    it = iterable
    last_index = len(it) - 1
    for i, val in enumerate(it):
        yield i == 0 or i == last_index, val
