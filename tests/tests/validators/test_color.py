from django.core.exceptions import ValidationError

from django_boost.test import TestCase
from django_boost.validators import validate_color_code

TEST_DATA = [
    ("#001122", None),
    ("00FF11", ValidationError),
    ("#R00000", ValidationError),
    ("prefix#001122", ValidationError),
    ("#001122suffix", ValidationError),
]


class TestColorCodeValidator(TestCase):

    def test_validates(self):
        for value, expected in TEST_DATA:
            with self.subTest(value=value):
                if expected is None:
                    self.assertIsNone(validate_color_code(value))
                else:
                    with self.assertRaises(expected):
                        validate_color_code(value)
