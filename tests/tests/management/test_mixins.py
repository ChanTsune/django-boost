from io import StringIO

from django.core.management.base import CommandError

from django_boost.core.management import BaseCommand
from django_boost.management.mixins import OutputFormatMixin
from django_boost.test import TestCase


class _RowCommand(OutputFormatMixin, BaseCommand):
    OUTPUT_FIELDS = ("a", "b")

    def get_row_data(self, obj, **options):
        return dict(obj)


class _IncompleteCommand(OutputFormatMixin, BaseCommand):
    OUTPUT_FIELDS = ("a", "b")

    def get_row_data(self, obj, **options):
        return {"a": "only-a"}


class OutputFormatMixinTests(TestCase):

    def test_get_row_data_is_abstract(self):
        with self.assertRaises(NotImplementedError):
            OutputFormatMixin().get_row_data(object())

    def test_default_print_text_renders_pipe_table(self):
        out = StringIO()
        command = _RowCommand(stdout=out)
        command.print_text([{"a": 1, "b": 2}])
        self.assertEqual(out.getvalue().splitlines(), ["a | b", "1 | 2"])

    def test_print_text_reports_missing_output_field(self):
        command = _IncompleteCommand(stdout=StringIO())
        with self.assertRaisesRegex(CommandError, "b"):
            command.print_text([object()])

    def test_print_delimited_reports_missing_output_field(self):
        command = _IncompleteCommand(stdout=StringIO())
        with self.assertRaisesRegex(CommandError, "b"):
            command.print_delimited([object()], ",")
