"""Mixins for django_boost's own management commands."""

from __future__ import annotations

import csv
from collections.abc import Iterable, Mapping
from io import StringIO
from typing import Any, ClassVar, TYPE_CHECKING

from django.core.management.base import CommandError, CommandParser, OutputWrapper

from django_boost.core.management import BaseCommand

if TYPE_CHECKING:
    _BaseCommandHost = BaseCommand
else:
    _BaseCommandHost = object


class OutputFormatMixin(_BaseCommandHost):
    """Add a ``--format`` option with shared text/csv/tsv rendering.

    Mix into a ``BaseCommand`` subclass -- it writes through ``self.stdout``
    provided by that base.
    Subclasses set ``OUTPUT_FIELDS`` and implement ``get_row_data``, which must
    return a mapping containing a key for every name in ``OUTPUT_FIELDS``.
    ``print_text`` defaults to a ``field | field`` table; override it for a
    custom layout (e.g. colored output). The delimited formats and the format
    dispatch are shared.
    """

    TEXT_FORMAT: ClassVar[str] = "text"
    DELIMITED_FORMATS: ClassVar[dict[str, str]] = {
        "csv": ",",
        "tsv": "\t",
    }
    OUTPUT_FIELDS: ClassVar[tuple[str, ...]] = ()

    def supported_formats(self) -> list[str]:  # noqa: D102
        return [self.TEXT_FORMAT, *self.DELIMITED_FORMATS]

    def add_format_option(self, parser: CommandParser) -> None:  # noqa: D102
        parser.add_argument('--format', choices=self.supported_formats(),
                            default=self.TEXT_FORMAT,
                            help="Output format.")

    def get_row_data(self, obj: Any, **options: Any) -> Mapping[str, Any]:  # noqa: D102
        raise NotImplementedError(
            "%s must implement get_row_data() returning a mapping with keys %s"
            % (type(self).__name__, tuple(self.OUTPUT_FIELDS)))

    def _row_values(self, obj: Any, **options: Any) -> list[Any]:
        data = self.get_row_data(obj, **options)
        missing = [field for field in self.OUTPUT_FIELDS if field not in data]
        if missing:
            raise CommandError(
                "%s.get_row_data() omitted OUTPUT_FIELDS: %s"
                % (type(self).__name__, ", ".join(missing)))
        return [data[field] for field in self.OUTPUT_FIELDS]

    def print_text(self, rows: Iterable[Any], **options: Any) -> None:  # noqa: D102
        self.stdout.write(" | ".join(self.OUTPUT_FIELDS))
        for obj in rows:
            self.stdout.write(
                " | ".join(str(value)
                           for value in self._row_values(obj, **options)))

    def print_delimited(self, rows: Iterable[Any], delimiter: str, **options: Any) -> None:  # noqa: D102
        stream = StringIO()
        writer = csv.writer(stream, delimiter=delimiter)
        writer.writerow(self.OUTPUT_FIELDS)
        for obj in rows:
            writer.writerow(self._row_values(obj, **options))
        self.stdout.write(stream.getvalue(), ending="")

    def print_formatted(self, rows: Iterable[Any], **options: Any) -> None:  # noqa: D102
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
    """Add a ``-y`` option and a ``confirm()`` helper that prompts unless it's set."""

    def add_confirm_option(self, parser: CommandParser) -> None:  # noqa: D102
        parser.add_argument('-y', action='store_true')

    def confirm(self, message: str, **options: Any) -> bool:  # noqa: D102
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


class QuitOptionMixin(_BaseCommandHost):
    """Add a ``-q``/``--quit`` option that silences ``self.stdout``/``self.stderr``."""

    def add_quit_option(self, parser: CommandParser) -> None:  # noqa: D102
        parser.add_argument('-q', '--quit', action='store_true',
                            help="Don't output to standard output.")

    def if_needed_make_quit(self, **options: Any) -> None:  # noqa: D102
        if options.get('quit', False):
            # BaseCommand.stdout/.stderr are OutputWrapper (its write() takes
            # an ending= kwarg plain StringIO.write doesn't); wrap the StringIO
            # instead of assigning it directly.
            self.stderr = self.stdout = OutputWrapper(StringIO())
