from django.test import SimpleTestCase

from django_boost.models.fields import ColorCodeField, ColorCodeFiled


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


class ColorCodeFiledDeprecationTests(SimpleTestCase):
    """`ColorCodeFiled` is the misspelled, deprecated alias of `ColorCodeField`."""

    def test_is_subclass_of_color_code_field(self):
        self.assertTrue(issubclass(ColorCodeFiled, ColorCodeField))

    def test_instantiation_warns(self):
        with self.assertWarns(DeprecationWarning):
            ColorCodeFiled()

    def test_still_functional(self):
        with self.assertWarns(DeprecationWarning):
            field = ColorCodeFiled(upper=True)
        self.assertEqual(field.max_length, 7)
