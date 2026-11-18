"""The removed UUID validator is no longer part of the public API."""

from importlib.util import find_spec

from django_boost import validators
from django_boost.test import TestCase


class RemovedUuidValidatorTests(TestCase):
    def test_validator_is_not_exported(self):
        self.assertNotIn("validate_uuid4", validators.__all__)
        self.assertFalse(hasattr(validators, "validate_uuid4"))

    def test_legacy_module_is_removed(self):
        self.assertIsNone(find_spec("django_boost.validators.uuid"))
