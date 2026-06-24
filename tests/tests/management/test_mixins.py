from django_boost.management.mixins import OutputFormatMixin
from django_boost.test import TestCase


class OutputFormatMixinTests(TestCase):

    def test_get_row_data_is_abstract(self):
        with self.assertRaises(NotImplementedError):
            OutputFormatMixin().get_row_data(object())

    def test_print_text_is_abstract(self):
        with self.assertRaises(NotImplementedError):
            OutputFormatMixin().print_text([])
