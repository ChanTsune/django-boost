from __future__ import annotations

import csv
from io import StringIO

from django.core.management.base import CommandError


class OutputFormatMixin:
    """Add a ``--format`` option with shared text/csv/tsv rendering.

    Subclasses set ``OUTPUT_FIELDS`` and implement ``get_row_data`` (a field
    name to value mapping for one row) and ``print_text`` (the human-readable
    layout). The delimited formats and the format dispatch are shared.
    """

    TEXT_FORMAT = "text"
    DELIMITED_FORMATS = {
        "csv": ",",
        "tsv": "\t",
    }
    OUTPUT_FIELDS = ()

    def supported_formats(self):
        return [self.TEXT_FORMAT, *self.DELIMITED_FORMATS]

    def add_format_option(self, parser):
        parser.add_argument('--format', choices=self.supported_formats(),
                            default=self.TEXT_FORMAT,
                            help="Output format.")

    def get_row_data(self, obj, **options):
        raise NotImplementedError

    def print_text(self, rows, **options):
        raise NotImplementedError

    def print_delimited(self, rows, delimiter, **options):
        stream = StringIO()
        writer = csv.writer(stream, delimiter=delimiter)
        writer.writerow(self.OUTPUT_FIELDS)
        for obj in rows:
            data = self.get_row_data(obj, **options)
            writer.writerow([data[field] for field in self.OUTPUT_FIELDS])
        self.stdout.write(stream.getvalue(), ending="")

    def print_formatted(self, rows, **options):
        output_format = options["format"]
        if output_format == self.TEXT_FORMAT:
            self.print_text(rows, **options)
        elif output_format in self.DELIMITED_FORMATS:
            self.print_delimited(
                rows, self.DELIMITED_FORMATS[output_format], **options)
        else:
            raise CommandError(
                "Unsupported format '%s'; choose from: %s"
                % (output_format, ", ".join(self.supported_formats())))


class ConfirmOptionMixin:

    def add_confirm_option(self, parser):
        parser.add_argument('-y', action='store_true')

    def confirm(self, message, **options):
        if not options.get('y', False):
            answer = None
            while not answer or answer not in "yn":
                answer = input(message + " [y/N] ")
                if not answer:
                    answer = "n"
                    break
                else:
                    answer = answer[0].lower()
            return answer == "y"
        return True


class QuitOptionMixin:

    def add_quit_option(self, parser):
        parser.add_argument('-q', '--quit', action='store_true',
                            help="Don't output to standard output.")

    def if_needed_make_quit(self, **options):
        if options.get('quit', False):
            self.stderr = self.stdout = StringIO()
