from uuid import uuid4

from django.core.exceptions import ValidationError

from django_boost.test import TestCase
from django_boost.validators import validate_uuid4


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
