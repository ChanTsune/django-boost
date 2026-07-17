"""The ``adminsitelog`` management command."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any, ClassVar

from django.contrib.admin.models import LogEntry
from django.core.exceptions import FieldError, ValidationError
from django.core.management.base import CommandError, CommandParser
from django.db.models import Model
from django.db.models.sql.query import get_field_names_from_opts  # type: ignore[attr-defined]
from django.utils.translation import gettext_lazy as _

from django_boost.core.management import BaseCommand
from django_boost.management.mixins import ConfirmOptionMixin, OutputFormatMixin
from django_boost.utils.attribute import getattr_chain, hasattr_chain

# get_field_names_from_opts is an internal Django helper django-stubs doesn't
# cover; the ignore above is the only way to use it under the plugin.


class Command(OutputFormatMixin, ConfirmOptionMixin, BaseCommand):
    """View and delete Django admin site log entries."""

    help = "Django admin site log"
    COMPARISON_OPERATION: ClassVar[dict[str, str]] = {
        "<=": "lte",
        ">=": "gte",
        "=": "exact",
        "<": "lt",
        ">": "gt",
    }
    OUTPUT_FIELDS: ClassVar[tuple[str, ...]] = ("id", "action", "detail", "user", "time")

    def get_sortable_fields(self, model: type[Model]) -> list[str]:  # noqa: D102
        return sorted(get_field_names_from_opts(model._meta))

    def get_log_entry_model(self) -> type[LogEntry]:
        """Return Django admin's ``LogEntry`` model, raising if ``django.contrib.admin`` isn't installed."""
        from django.apps import apps
        if not apps.is_installed("django.contrib.admin"):
            raise CommandError(
                "adminsitelog requires 'django.contrib.admin' in "
                "INSTALLED_APPS.")
        from django.contrib.admin.models import LogEntry
        return LogEntry

    def get_sortable_fields_help(self) -> str:
        """Return the sortable field names for ``--help``, or a hint if admin isn't installed."""
        from django.apps import apps
        if not apps.is_installed("django.contrib.admin"):
            return "(requires 'django.contrib.admin' in INSTALLED_APPS)"
        return ", ".join(self.get_sortable_fields(self.get_log_entry_model()))

    def _parse_filter(self, condition: str) -> dict[str, str]:
        # Split on the operator that appears leftmost in the condition (so a
        # comparison operator inside the value is not mistaken for the
        # field/value boundary); at the same position prefer the longer
        # operator so '>=' wins over '>'.
        best: tuple[tuple[int, int], str] | None = None
        for op in self.COMPARISON_OPERATION:
            index = condition.find(op)
            if index != -1 and (best is None or (index, -len(op)) < best[0]):
                best = ((index, -len(op)), op)
        if best is None:
            raise CommandError(
                "Unsupported filter operation in '%s'; "
                "--filter and --exclude support: %s"
                % (condition, ", ".join(self.COMPARISON_OPERATION)))
        index, op = best[0][0], best[1]
        lookup = self.COMPARISON_OPERATION[op]
        return {"%s__%s" % (condition[:index], lookup):
                condition[index + len(op):]}

    def parse_filter(self, conditions: Iterable[str]) -> dict[str, str]:  # noqa: D102
        parsed: dict[str, str] = {}
        for condition in conditions:
            parsed.update(self._parse_filter(condition))
        return parsed

    def get_row_data(self, obj: LogEntry, **options: Any) -> dict[str, Any]:
        """Map a ``LogEntry`` to the OUTPUT_FIELDS row dict, classifying it as Added/Changed/Deleted."""
        if obj.is_addition():
            action = "Added"
            detail = obj.object_repr
        elif obj.is_change():
            action = "Changed"
            detail = "%s - %s" % (obj.object_repr,
                                  obj.get_change_message())
        else:  # log.is_deletion
            action = "Deleted"
            detail = obj.object_repr
        return {
            "id": obj.id,
            "action": action,
            "detail": detail,
            "user": self._get_user_name(obj.user, options['name_field']),
            "time": obj.action_time,
        }

    def print_log(self, log: LogEntry, **options: Any) -> None:
        """Write one colorized ``id | action | object | user | time`` line for ``log``."""
        fmt = "{id} | {action} | {object} | {user} | {time}"
        fmap = self.get_row_data(log, **options)
        if fmap["action"] == "Added":
            fmap["action"] = self.style.SUCCESS(fmap["action"])
        elif fmap["action"] == "Changed":
            fmap["action"] = self.style.WARNING(fmap["action"])
        else:
            fmap["action"] = self.style.ERROR(fmap["action"])
        fmap["object"] = fmap.pop("detail")
        self.stdout.write(fmt.format_map(fmap))

    def print_text(self, rows: Iterable[Any], **options: Any) -> None:  # noqa: D102
        self.stdout.write(" | ".join(self.OUTPUT_FIELDS))
        for log in rows:
            self.print_log(log, **options)

    def _get_user_name(self, user: Any, name_field: str | None = None) -> Any:
        if name_field is not None:
            if hasattr_chain(user, name_field):
                return getattr_chain(user, name_field)
            raise CommandError(
                "--name_field '%s' is not an attribute of %s."
                % (name_field, type(user).__name__))
        name_fields = ["username", "email"]
        for field in name_fields:
            if hasattr(user, field):
                return getattr(user, field)
        return None

    def add_arguments(self, parser: CommandParser) -> None:  # noqa: D102
        supported_fields_str = self.get_sortable_fields_help()
        parser.add_argument('-d', '--delete',
                            action='store_true', help='Delete displayed logs.')
        parser.add_argument('--filter', nargs='+',
                            type=str, default=[],
                            help="""Filter the Log to be displayed.
                                    Supported field is %s.
                                    e.g. "action_time>=2019-8-22" """
                            % supported_fields_str)
        parser.add_argument('--exclude', nargs='+',
                            type=str, default=[],
                            help="""Exclude the Log to be displayed.
                                    Supported field is same as --filter.
                                    e.g. "user__username=admin" """)
        parser.add_argument('--order_by', nargs='+',
                            type=str, default=['action_time'],
                            help="""Order of Log to be displayed.
                                    Supported field is %s.
                                    e.g. "-action_flag" """
                            % supported_fields_str)
        parser.add_argument('--name_field', type=str,
                            default=None,
                            help="""user name field.
                                    e.g. "--name_field email",
                                    "--name_field profile.phone" """)
        self.add_format_option(parser)
        self.add_confirm_option(parser)

    def handle(self, *args: Any, **options: Any) -> None:  # noqa: D102
        LogEntry = self.get_log_entry_model()
        queryset = LogEntry.objects.all()

        try:
            queryset = queryset.filter(**self.parse_filter(options['filter']))
            queryset = queryset.exclude(**self.parse_filter(options['exclude']))
            queryset = queryset.order_by(*options['order_by'])
        except (FieldError, ValidationError, ValueError) as e:
            raise CommandError(str(e))

        if queryset.count() == 0:
            self.stderr.write('No logs')
            return
        self.print_formatted(queryset, **options)
        if options['delete']:
            if self.confirm(message=str(_("Do you want to delete these logs")), **options):
                queryset.delete()
                self.stderr.write('delete complete')
            else:
                self.stderr.write('operation canceled')
