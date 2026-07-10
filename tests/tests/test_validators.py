from types import FunctionType
from uuid import uuid4

from django.core.exceptions import ValidationError

from django_boost.test import TestCase
from django_boost.validators import (
    ContainAnyValidator, JsonValidator, NonZeroValidator,
    validate_color_code, validate_json, validate_non_zero, validate_uuid4,
)

TEST_DATA = [
    (validate_color_code, "#001122", None),
    (validate_color_code, "00FF11", ValidationError),
    (validate_color_code, "#R00000", ValidationError),
    (validate_color_code, "prefix#001122", ValidationError),
    (validate_color_code, "#001122suffix", ValidationError),

    (validate_json, '{}', None),
    (validate_json, '{"a":"apple"}', None),
    (validate_json, '{"a":"apple",}', ValidationError),
    (validate_json, "{'a':'apple'}", ValidationError),
    (validate_json, 1, TypeError),

    (ContainAnyValidator("1"), "123", None),
    (ContainAnyValidator("02"), "123", None),
    (ContainAnyValidator("4"), "123", ValidationError),
    (ContainAnyValidator(("4", "5")), "123", ValidationError),

    (validate_non_zero, 0, ValidationError),
    (validate_non_zero, 1, None),
    (validate_non_zero, -1, None),
    (validate_non_zero, 100, None),
    (validate_non_zero, -100, None),
    (validate_non_zero, None, None),
]


class TestValidator(TestCase):

    def test_validators(self):
        for validator, value, expected in TEST_DATA:
            name = validator.__name__ if isinstance(
                validator, FunctionType) else validator.__class__.__name__
            exception_expected = expected is not None and issubclass(
                expected, Exception)
            with self.subTest(name, value=value):
                if exception_expected:
                    with self.assertRaises(expected):
                        validator(value)
                else:
                    self.assertEqual(expected, validator(value))

    def test_validator_message(self):
        cases = [
            (ContainAnyValidator("1", "custom message with %s"), "0", "custom message with 1"),
            (JsonValidator("custom message"), "", "custom message"),
            (NonZeroValidator("custom message"), 0, "custom message"),
        ]
        for validator, value, message in cases:
            name = validator.__class__.__name__
            with self.subTest(name, value=value):
                with self.assertRaisesMessage(ValidationError, message):
                    validator(value)

    def test_contain_any_validators_are_comparable(self):
        # Regression: BaseValidator.__eq__ reads limit_value.
        self.assertEqual(
            ContainAnyValidator(("a", "b")), ContainAnyValidator(("a", "b")))
        self.assertNotEqual(
            ContainAnyValidator(("a",)), ContainAnyValidator(("b",)))

    def test_contain_any_custom_message_without_placeholder(self):
        # A custom message with no %-placeholder must still raise
        # ValidationError, not a string-formatting TypeError.
        validator = ContainAnyValidator(("a", "b"), "Supply a valid token")
        with self.assertRaisesMessage(ValidationError, "Supply a valid token"):
            validator("xyz")

    def test_json_and_non_zero_validators_are_comparable(self):
        # Regression: BaseValidator.__eq__ reads limit_value, which was never
        # initialized because __init__ skipped super().__init__().
        self.assertEqual(JsonValidator(), JsonValidator())
        self.assertEqual(NonZeroValidator(), NonZeroValidator())
        self.assertNotEqual(JsonValidator(), JsonValidator("other"))
        self.assertNotEqual(NonZeroValidator(), NonZeroValidator("other"))


class NonZeroValidatorDeconstruct(TestCase):
    """`NonZeroValidator` serializes to its public path for migrations."""

    def test_deconstruct_reports_public_path(self):
        path, args, kwargs = NonZeroValidator().deconstruct()
        self.assertEqual(path, "django_boost.validators.NonZeroValidator")


class ValidateUuid4Deprecation(TestCase):
    """`validate_uuid4` is deprecated; removal is planned for django-boost 4.0."""

    def test_warns_on_call(self):
        with self.assertWarns(DeprecationWarning):
            validate_uuid4(str(uuid4()))

    def test_still_validates_under_warning(self):
        with self.assertWarns(DeprecationWarning):
            self.assertIsNone(validate_uuid4(str(uuid4())))
        with self.assertWarns(DeprecationWarning):
            with self.assertRaises(ValidationError):
                validate_uuid4("not-a-uuid")
