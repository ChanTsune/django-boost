from __future__ import annotations

import decimal
from typing import ClassVar, Generic, TypeVar

_T = TypeVar('_T')

# branch 1: integer part has a non-zero digit (fraction optional)
# branch 2: integer part is all zeros, but the fraction has a non-zero digit
POSITIVE = r'(?:[0-9]*[1-9][0-9]*(?:\.[0-9]+)?|0+\.[0-9]*[1-9][0-9]*)'
# the whole value is zero, e.g. 0, 00, 0.0, 0.00
ZERO = r'0+(?:\.0+)?'


class BaseSignedNumericConverter(Generic[_T]):
    """Shared behavior for signed decimal-notation numeric path converters.

    Subclasses declare ``regex`` and ``_parse`` (a ``str -> _T`` callable,
    wrapped in ``staticmethod``). Sign/zero classification looks at the
    whole value (integer part and fractional part together) rather than
    the integer part alone, so e.g. ``0.5`` counts as positive even though
    its integer part is ``0``.
    """

    regex: ClassVar[str]
    # Not ClassVar: PEP 526 disallows a type variable inside ClassVar, and
    # mypy 1.x enforces it (mypy 2.x currently doesn't, but don't rely on that).
    _parse: staticmethod[[str], _T]

    def to_python(self, value: str) -> _T:  # noqa: D102
        return self._parse(value)

    def to_url(self, value: _T | str) -> str:  # noqa: D102
        # A string is passed through verbatim, so a malformed one still
        # fails the reverse match. For an actual numeric value, str(value)
        # can switch to exponential notation at extreme magnitudes (a float
        # < 1e-4 or >= 1e16, or a Decimal with a positive exponent), which
        # the fixed-point ``regex`` above rejects; re-rendering it through
        # Decimal keeps it in fixed-point notation without rounding it.
        if isinstance(value, str):
            return value
        return format(decimal.Decimal(str(value)), 'f')
