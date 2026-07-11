from django.core.exceptions import ValidationError

from django_boost.test import TestCase
from django_boost.validators import JsonValidator, validate_json

TEST_DATA = [
    ('{}', None),
    ('{"a":"apple"}', None),
    ('{"a":"apple",}', ValidationError),
    ("{'a':'apple'}", ValidationError),
    (1, TypeError),
]


class TestJsonValidator(TestCase):

    def test_validates(self):
        for value, expected in TEST_DATA:
            with self.subTest(value=value):
                if expected is None:
                    self.assertIsNone(validate_json(value))
                else:
                    with self.assertRaises(expected):
                        validate_json(value)

    def test_validator_message(self):
        validator = JsonValidator("custom message")
        with self.assertRaisesMessage(ValidationError, "custom message"):
            validator("")

    def test_are_comparable(self):
        # Regression: BaseValidator.__eq__ reads limit_value, which was
        # never initialized because __init__ skipped super().__init__().
        self.assertEqual(JsonValidator(), JsonValidator())
        self.assertNotEqual(JsonValidator(), JsonValidator("other"))
