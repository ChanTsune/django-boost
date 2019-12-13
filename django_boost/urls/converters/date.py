from datetime import datetime

REGEX_LEAP_YEAR = r"(?!0)(\d*((0[48]|[2468][048]|[13579][26])(00)?|0000)|[048]?(00)?)"
NON_ZERO_YEAR = r"(?!0)(\d)+"

REGEX_MONTH_31 = r"(1|3|5|7|8|10|12)"
REGEX_DAY_31 = r"([1-9]|[12][0-9]|3[01])"
REGEX_DATE_31 = REGEX_MONTH_31 + "/" + REGEX_DAY_31

REGEX_MONTH_30 = r"(4|6|9|11)"
REGEX_DAY_30 = r"([1-9]|[12][0-9]|30)"
REGEX_DATE_30 = REGEX_MONTH_30 + "/" + REGEX_DAY_30

REGEX_MONTH_29 = REGEX_MONTH_28 = '2'
REGEX_DAY_29 = r"([1-9]|[12][0-9])"
REGEX_DAY_28 = r"([1-9]|1[0-9]|2[0-8])"

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
    regex = REGEX_DATE

    def to_url(self, value):
        if isinstance(value, datetime):
            return datetime.strftime(value, "%Y/%m/%d")
        return str(value)

    def to_python(self, value):
        if isinstance(value, datetime):
            return value
        return datetime.strptime(value, "%Y/%m/%d")
