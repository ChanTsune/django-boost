from types import FunctionType
from uuid import uuid4

from django.core.exceptions import ValidationError

from django_boost.test import TestCase
from django_boost.validators import (
    ContainAnyValidator, JsonValidator,
    validate_color_code, validate_json, validate_uuid4,
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
        ]
        for validator, value, message in cases:
            name = validator.__class__.__name__
            with self.subTest(name, value=value):
                with self.assertRaisesMessage(ValidationError, message):
                    validator(value)


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
