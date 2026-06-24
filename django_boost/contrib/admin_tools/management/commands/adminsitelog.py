from __future__ import annotations

from django.core.management.base import CommandError
from django.db.models.sql.query import get_field_names_from_opts
from django.utils.translation import gettext_lazy as _

from django_boost.core.management import BaseCommand
from django_boost.management.mixins import ConfirmOptionMixin, OutputFormatMixin
from django_boost.utils.attribute import getattr_chain, hasattr_chain


class Command(OutputFormatMixin, ConfirmOptionMixin, BaseCommand):
    """View and delete Django admin site log entries."""

    help = "Django admin site log"
    COMPARISON_OPERATION = {"<=": "lte",
                            ">=": "gte",
                            "=": "exact",
                            "<": "lt",
                            ">": "gt", }
    OUTPUT_FIELDS = ("id", "action", "detail", "user", "time")

    def get_sortable_fields(self, model):
        return sorted(get_field_names_from_opts(model._meta))

    def get_log_entry_model(self):
        from django.apps import apps
        if not apps.is_installed("django.contrib.admin"):
            raise CommandError(
                "adminsitelog requires 'django.contrib.admin' in "
                "INSTALLED_APPS.")
        from django.contrib.admin.models import LogEntry
        return LogEntry

    def get_sortable_fields_help(self):
        from django.apps import apps
        if not apps.is_installed("django.contrib.admin"):
            return "(requires 'django.contrib.admin' in INSTALLED_APPS)"
        return ", ".join(self.get_sortable_fields(self.get_log_entry_model()))

    def _parse_filter(self, condition):
        for op in self.COMPARISON_OPERATION.keys():
            field, op, value = condition.partition(op)
            op = self.COMPARISON_OPERATION.get(op, None)
            if op is not None:
                return {"%s__%s" % (field, op): value}
        raise CommandError(
            "Unsupported filter operation in '%s'; "
            "--filter and --exclude support: %s"
            % (condition, ", ".join(self.COMPARISON_OPERATION)))

    def parse_filter(self, conditions):
        parsed = {}
        for condition in conditions:
            parsed.update(self._parse_filter(condition))
        return parsed

    def get_row_data(self, log, **options):
        if log.is_addition():
            action = "Added"
            detail = log.object_repr
        elif log.is_change():
            action = "Changed"
            detail = "%s - %s" % (log.object_repr,
                                  log.get_change_message())
        else:  # log.is_deletion
            action = "Deleted"
            detail = log.object_repr
        return {
            "id": log.id,
            "action": action,
            "detail": detail,
            "user": self._get_user_name(log.user, options['name_field']),
            "time": log.action_time,
        }

    def print_log(self, log, **options):
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

    def print_text(self, rows, **options):
        self.stdout.write(" | ".join(self.OUTPUT_FIELDS))
        for log in rows:
            self.print_log(log, **options)

    def _get_user_name(self, user, name_field=None):
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

    def add_arguments(self, parser):
        supported_fields_str = self.get_sortable_fields_help()
        parser.add_argument('-d', '--delete',
                            action='store_true', help='Delete displayed logs.')
        parser.add_argument('--filter', nargs='+',
                            type=str, default=[],
                            help="""Filter the Log to be displayed.
                                    Supported filed is %s.
                                    e.g. "action_time>=2019-8-22" """
                            % supported_fields_str)
        parser.add_argument('--exclude', nargs='+',
                            type=str, default=[],
                            help="""Exclude the Log to be displayed.
                                    Supported filed is same as --filter.
                                    e.g. "user__username=admin" """)
        parser.add_argument('--order_by', nargs='+',
                            type=str, default=['action_time'],
                            help="""Order of Log to be displayed.
                                    Supported filed is %s.
                                    e.g. "-action_flag" """
                            % supported_fields_str)
        parser.add_argument('--name_field', type=str,
                            default=None,
                            help="""user name field.
                                    e.g. "--name_field email",
                                    "--name_field profile.phone" """)
        self.add_format_option(parser)
        self.add_confirm_option(parser)

    def handle(self, *args, **options):
        LogEntry = self.get_log_entry_model()
        queryset = LogEntry.objects.all()

        queryset = queryset.filter(**self.parse_filter(options['filter']))
        queryset = queryset.exclude(**self.parse_filter(options['exclude']))

        queryset = queryset.order_by(*options['order_by'])

        if queryset.count() == 0:
            self.stderr.write('No logs')
            return
        self.print_formatted(queryset, **options)
        if options['delete']:
            if self.confirm(message=_("Do you want to delete these logs"), **options):
                queryset.delete()
                self.stderr.write('delete complete')
            else:
                self.stderr.write('operation canceled')
