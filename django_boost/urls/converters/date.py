"""Extensions for Django's ``django.urls`` path converters."""

from __future__ import annotations

from datetime import datetime
from typing import ClassVar

REGEX_LEAP_YEAR = r"(([48](00)?)|(([2468][048]|[13579][26])(00)?)|([1-9][0-9]?(0[48]|[2468][048]|[13579][26])))"
NON_ZERO_YEAR = r"[1-9]([0-9]){,3}"

REGEX_MONTH_31 = r"(0?[13578]|10|12)"
REGEX_DAY_31 = r"(0?[1-9]|[12][0-9]|3[01])"
REGEX_DATE_31 = REGEX_MONTH_31 + "/" + REGEX_DAY_31

REGEX_MONTH_30 = r"(0?[469]|11)"
REGEX_DAY_30 = r"(0?[1-9]|[12][0-9]|30)"
REGEX_DATE_30 = REGEX_MONTH_30 + "/" + REGEX_DAY_30

REGEX_MONTH_29 = REGEX_MONTH_28 = r"0?2"
REGEX_DAY_29 = r"(0?[1-9]|[12][0-9])"
REGEX_DAY_28 = r"(0?[1-9]|1[0-9]|2[0-8])"

REGEX_DATE_29 = REGEX_MONTH_29 + "/" + REGEX_DAY_29
REGEX_DATE_28 = REGEX_MONTH_28 + "/" + REGEX_DAY_28

REGEX_DATE = '({LEAP_YEAR}/({DATE_31}|{DATE_30}|{DATE_29})|{NON_ZERO}/({DATE_31}|{DATE_30}|{DATE_28}))'
REGEX_DATE = REGEX_DATE.format(
    LEAP_YEAR=REGEX_LEAP_YEAR,
    NON_ZERO=NON_ZERO_YEAR,
    DATE_31=REGEX_DATE_31,
    DATE_30=REGEX_DATE_30,
    DATE_29=REGEX_DATE_29,
    DATE_28=REGEX_DATE_28)


class DateConverter:
    """URL converter for calendar dates in ``Y/M/D`` format, validating real dates via ``regex``."""

    regex: ClassVar[str] = REGEX_DATE

    def to_url(self, value: datetime | str) -> str:
        """Render ``value`` as ``Y/M/D``, accepting either a ``datetime`` or an already-formatted string."""
        if isinstance(value, datetime):
            return f"{value.year}/{value.month}/{value.day}"
        return str(value)

    def to_python(self, value: datetime | str) -> datetime:
        """Parse a ``Y/M/D`` string into a ``datetime``, passing an already-parsed ``datetime`` through."""
        if isinstance(value, datetime):
            return value
        # strptime's %Y needs 4 digits, but the regex accepts 1-4; build the
        # date directly so every year the pattern matches is parseable.
        year, month, day = value.split("/")
        return datetime(int(year), int(month), int(day))
