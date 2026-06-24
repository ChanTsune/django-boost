from __future__ import annotations

import csv
from io import StringIO

from django.contrib.admin.models import LogEntry
from django.core.management.base import CommandError
from django.db.models.sql.query import get_field_names_from_opts
from django.utils.translation import gettext_lazy as _

from django_boost.core.management import BaseCommand
from django_boost.management.mixins import ConfirmOptionMixin
from django_boost.utils.attribute import getattr_chain, hasattr_chain


class Command(ConfirmOptionMixin, BaseCommand):
    """Django admin site log cli."""

    help = "Django admin site log"
    COMPARISON_OPERATION = {"<=": "lte",
                            ">=": "gte",
                            "=": "exact",
                            "<": "lt",
                            ">": "gt", }
    TEXT_FORMAT = "text"
    OUTPUT_FIELDS = ("id", "action", "detail", "user", "time")
    DELIMITED_FORMATS = {
        "csv": ",",
        "tsv": "\t",
    }

    def get_sortable_fields(self, model):
        return sorted(get_field_names_from_opts(model._meta))

    def _parse_filter(self, condition):
        for op in self.COMPARISON_OPERATION.keys():
            field, op, value = condition.partition(op)
            op = self.COMPARISON_OPERATION.get(op, None)
            if op is not None:
                return {"%s__%s" % (field, op): value}
        raise Exception("""
        Unsupported operation '%s'
        --filter and --exclude supported %s
        """ % (field, ",".join(self.COMPARISON_OPERATION.keys())))

    def parse_filter(self, conditions):
        parsed = {}
        for condition in conditions:
            parsed.update(self._parse_filter(condition))
        return parsed

    def get_log_data(self, log, **options):
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
        fmap = self.get_log_data(log, **options)
        if fmap["action"] == "Added":
            fmap["action"] = self.style.SUCCESS(fmap["action"])
        elif fmap["action"] == "Changed":
            fmap["action"] = self.style.WARNING(fmap["action"])
        else:
            fmap["action"] = self.style.ERROR(fmap["action"])
        fmap["object"] = fmap.pop("detail")
        self.stdout.write(fmt.format_map(fmap))

    def print_text_logs(self, queryset, **options):
        self.stdout.write("id | action | detail | user | time")
        for log in queryset:
            self.print_log(log, **options)

    def print_delimited_logs(self, queryset, delimiter, **options):
        stream = StringIO()
        writer = csv.writer(stream, delimiter=delimiter)
        writer.writerow(self.OUTPUT_FIELDS)
        for log in queryset:
            data = self.get_log_data(log, **options)
            writer.writerow([data[field] for field in self.OUTPUT_FIELDS])
        self.stdout.write(stream.getvalue(), ending="")

    def supported_formats(self):
        return [self.TEXT_FORMAT, *self.DELIMITED_FORMATS]

    def print_logs(self, queryset, **options):
        output_format = options["format"]
        if output_format == self.TEXT_FORMAT:
            self.print_text_logs(queryset, **options)
        elif output_format in self.DELIMITED_FORMATS:
            self.print_delimited_logs(
                queryset, self.DELIMITED_FORMATS[output_format], **options)
        else:
            raise CommandError(
                "Unsupported format '%s'; choose from: %s"
                % (output_format, ", ".join(self.supported_formats())))

    def _get_user_name(self, user, name_field=None):
        if name_field is not None:
            if hasattr_chain(user, name_field):
                return getattr_chain(user, name_field)
            raise AttributeError("'%s' has no attribute '%s'" %
                                 (user.__class__, name_field))
        name_fields = ["username", "email"]
        for field in name_fields:
            if hasattr(user, field):
                return user.username

    def add_arguments(self, parser):
        supported_fields = self.get_sortable_fields(LogEntry)
        supported_fields_str = ", ".join(supported_fields)
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
        parser.add_argument('--format', choices=self.supported_formats(),
                            default=self.TEXT_FORMAT,
                            help="Output format.")
        self.add_confirm_option(parser)

    def handle(self, *args, **options):
        queryset = LogEntry.objects.all()

        queryset = queryset.filter(**self.parse_filter(options['filter']))
        queryset = queryset.exclude(**self.parse_filter(options['exclude']))

        queryset = queryset.order_by(*options['order_by'])

        if queryset.count() == 0:
            self.stderr.write('No logs')
            return
        self.print_logs(queryset, **options)
        if options['delete']:
            if self.confirm(message=_("Do you want to delete these logs"), **options):
                queryset.delete()
                self.stderr.write('delete complete')
            else:
                self.stderr.write('operation canceled')
