from django.core.exceptions import ValidationError

from django_boost.test import TestCase
from django_boost.validators import ContainAnyValidator

TEST_DATA = [
    (ContainAnyValidator("1"), "123", None),
    (ContainAnyValidator("02"), "123", None),
    (ContainAnyValidator("4"), "123", ValidationError),
    (ContainAnyValidator(("4", "5")), "123", ValidationError),
]


class TestContainAnyValidator(TestCase):

    def test_validates(self):
        for validator, value, expected in TEST_DATA:
            with self.subTest(value=value):
                if expected is None:
                    self.assertIsNone(validator(value))
                else:
                    with self.assertRaises(expected):
                        validator(value)

    def test_validator_message(self):
        validator = ContainAnyValidator("1", "custom message with %s")
        with self.assertRaisesMessage(
                ValidationError, "custom message with 1"):
            validator("0")

    def test_are_comparable(self):
        # Regression: BaseValidator.__eq__ reads limit_value.
        self.assertEqual(
            ContainAnyValidator(("a", "b")), ContainAnyValidator(("a", "b")))
        self.assertNotEqual(
            ContainAnyValidator(("a",)), ContainAnyValidator(("b",)))

    def test_custom_message_without_placeholder(self):
        # A custom message with no %-placeholder must still raise
        # ValidationError, not a string-formatting TypeError.
        validator = ContainAnyValidator(("a", "b"), "Supply a valid token")
        with self.assertRaisesMessage(ValidationError, "Supply a valid token"):
            validator("xyz")
