from django.test import SimpleTestCase

import django_boost.models.fields as boost_fields
from django_boost.models.fields import ColorCodeField


class ColorCodeFieldTests(SimpleTestCase):

    def test_max_length_is_forced(self):
        self.assertEqual(ColorCodeField().max_length, 7)

    def test_upper_and_lower_are_mutually_exclusive(self):
        with self.assertRaises(AssertionError):
            ColorCodeField(upper=True, lower=True)

    def test_upper_keeps_none(self):
        self.assertIsNone(ColorCodeField(upper=True).to_python(None))

    def test_lower_keeps_none(self):
        self.assertIsNone(ColorCodeField(lower=True).to_python(None))

    def test_deconstruct_preserves_upper(self):
        name, path, args, kwargs = ColorCodeField(upper=True).deconstruct()
        self.assertTrue(kwargs.get("upper"))
        rebuilt = ColorCodeField(*args, **kwargs)
        self.assertEqual(rebuilt.to_python("#abcdef"), "#ABCDEF")

    def test_deconstruct_preserves_lower(self):
        name, path, args, kwargs = ColorCodeField(lower=True).deconstruct()
        self.assertTrue(kwargs.get("lower"))
        rebuilt = ColorCodeField(*args, **kwargs)
        self.assertEqual(rebuilt.to_python("#ABCDEF"), "#abcdef")

    def test_deconstruct_omits_flags_by_default(self):
        name, path, args, kwargs = ColorCodeField().deconstruct()
        self.assertNotIn("upper", kwargs)
        self.assertNotIn("lower", kwargs)


class RemovedColorCodeFiledTests(SimpleTestCase):
    def test_misspelled_alias_is_no_longer_exported(self):
        self.assertFalse(hasattr(boost_fields, "ColorCodeFiled"))

    def test_canonical_field_still_works(self):
        field = ColorCodeField(upper=True)
        self.assertEqual(field.to_python("#abcdef"), "#ABCDEF")
