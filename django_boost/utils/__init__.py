"""General-purpose helper functions and classes."""

from __future__ import annotations

from collections.abc import Container, Iterable, Iterator, Sequence
from typing import TypeGuard, TypeVar

__all__ = ["Loop", "contain_any", "isiterable", "loop"]

_T = TypeVar("_T")


class Loop(Iterator[tuple["Loop[_T]", _T]]):
    """Django template like loop object."""

    # Per-iteration state; only valid after the first __next__ call.
    counter0: int
    counter: int
    revcounter: int
    revcounter0: int
    first: bool
    last: bool

    def __init__(self, iterable: Sequence[_T]) -> None:
        """Wrap ``iterable`` in an ``enumerate()`` to track position per iteration."""
        self.iterable = enumerate(iterable)
        self.length = len(iterable)

    def __iter__(self) -> Loop[_T]:
        return self

    def __next__(self) -> tuple[Loop[_T], _T]:
        i, item = next(self.iterable)
        # Shortcuts for current loop iteration number.
        self.counter0 = i
        self.counter = i + 1
        # Reverse counter iteration numbers.
        self.revcounter = self.length - i
        self.revcounter0 = self.length - i - 1
        # Boolean values designating first and last times through loop.
        self.first = (i == 0)
        self.last = (i == self.length - 1)
        return self, item


def loop(iterable: Sequence[_T]) -> Loop[_T]:
    """Provide features such as Django template like loop."""
    return Loop(iterable)


def isiterable(obj: object) -> TypeGuard[Iterable[object]]:
    """Return `True` if `obj` is iterable object, `False` otherwise."""
    try:
        iter(obj)  # type: ignore[call-overload]  # probe iterability of an arbitrary object
    except TypeError:
        return False
    return True


def contain_any(container: Container[object], elements: Iterable[object]) -> bool:
    """Return `True` if any of the `elements` are contained in `container`, `False` otherwise."""
    return any(e in container for e in elements)
