from types import FunctionType
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.test import TestCase

from django_boost.validators import (
    validate_color_code, validate_json, validate_uuid4)

TEST_DATA = [
    (validate_color_code, "#001122", None),
    (validate_color_code, "00FF11", ValidationError),
    (validate_color_code, "#R00000", ValidationError),

    (validate_json, '{}', None),
    (validate_json, '{"a":"apple"}', None),
    (validate_json, '{"a":"apple",}', ValidationError),
    (validate_json, "{'a':'apple'}", ValidationError),

    (validate_uuid4, str(uuid4()), None),
    (validate_uuid4, "59cF05e3-fb29-4be8-af18-da9c94b1964d", ValidationError),
    (validate_uuid4, "5de21727-8c45-4380-a44d-adc370-e6288", ValidationError),
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
