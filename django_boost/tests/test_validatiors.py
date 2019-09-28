from django.core.exceptions import ValidationError
from django.test import TestCase

from django_boost.validators import (
    validate_color_code, validate_json, validate_uuid4)


class TestValidator(TestCase):

    def test_validate_color_code(self):
        with self.assertRaises(ValidationError):
            validate_color_code("00FF11")
        
        with self.assertRaises(ValidationError):
            validate_color_code("#R00000")

    def test_validate_json(self):
        with self.assertRaises(ValidationError):
            validate_json('{"a":"apple",}')
        
        with self.assertRaises(ValidationError):
            validate_json("{'a':'apple'}")

    def test_validate_uuid4(self):
        with self.assertRaises(ValidationError):
            validate_uuid4("59cF05e3-fb29-4be8-af18-da9c94b1964d")
        
        with self.assertRaises(ValidationError):
            validate_uuid4("5de21727-8c45-4380-a44d-adc370-e6288")
