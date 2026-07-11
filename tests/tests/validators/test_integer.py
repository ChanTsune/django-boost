from django.core.exceptions import ValidationError

from django_boost.test import TestCase
from django_boost.validators import NonZeroValidator, validate_non_zero

TEST_DATA = [
    (0, ValidationError),
    (1, None),
    (-1, None),
    (100, None),
    (-100, None),
    (None, None),
]


class TestNonZeroValidator(TestCase):

    def test_validates(self):
        for value, expected in TEST_DATA:
            with self.subTest(value=value):
                if expected is None:
                    self.assertIsNone(validate_non_zero(value))
                else:
                    with self.assertRaises(expected):
                        validate_non_zero(value)

    def test_validator_message(self):
        validator = NonZeroValidator("custom message")
        with self.assertRaisesMessage(ValidationError, "custom message"):
            validator(0)

    def test_are_comparable(self):
        # Regression: BaseValidator.__eq__ reads limit_value, which was
        # never initialized because __init__ skipped super().__init__().
        self.assertEqual(NonZeroValidator(), NonZeroValidator())
        self.assertNotEqual(NonZeroValidator(), NonZeroValidator("other"))


class NonZeroValidatorDeconstruct(TestCase):
    """`NonZeroValidator` serializes to its public path for migrations."""

    def test_deconstruct_reports_public_path(self):
        path, args, kwargs = NonZeroValidator().deconstruct()
        self.assertEqual(path, "django_boost.validators.NonZeroValidator")
