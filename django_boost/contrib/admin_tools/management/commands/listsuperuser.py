from __future__ import annotations

import csv
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management.base import CommandError

from django_boost.core.management import BaseCommand


class Command(BaseCommand):
    """List super users with audit-relevant fields."""

    help = "List super users."
    TEXT_FORMAT = "text"
    OUTPUT_FIELDS = ("email", "active", "staff", "last_login")
    DELIMITED_FORMATS = {
        "csv": ",",
        "tsv": "\t",
    }

    def supported_formats(self):
        return [self.TEXT_FORMAT, *self.DELIMITED_FORMATS]

    def add_arguments(self, parser):
        parser.add_argument('--format', choices=self.supported_formats(),
                            default=self.TEXT_FORMAT,
                            help="Output format.")

    def get_queryset(self):
        User = get_user_model()
        return User.objects.filter(
            is_superuser=True).order_by(User.USERNAME_FIELD)

    def get_user_data(self, user):
        email_field = user.get_email_field_name()
        return {
            "email": getattr(user, email_field, "") or "",
            "active": "yes" if user.is_active else "no",
            "staff": "yes" if user.is_staff else "no",
            "last_login": str(user.last_login) if user.last_login else "(never)",
        }

    def print_text(self, queryset):
        self.stdout.write(" | ".join(self.OUTPUT_FIELDS))
        for user in queryset:
            data = self.get_user_data(user)
            self.stdout.write(
                " | ".join(str(data[field]) for field in self.OUTPUT_FIELDS))

    def print_delimited(self, queryset, delimiter):
        stream = StringIO()
        writer = csv.writer(stream, delimiter=delimiter)
        writer.writerow(self.OUTPUT_FIELDS)
        for user in queryset:
            data = self.get_user_data(user)
            writer.writerow([data[field] for field in self.OUTPUT_FIELDS])
        self.stdout.write(stream.getvalue(), ending="")

    def handle(self, *args, **options):
        output_format = options["format"]
        queryset = self.get_queryset()
        if output_format == self.TEXT_FORMAT:
            self.print_text(queryset)
        elif output_format in self.DELIMITED_FORMATS:
            self.print_delimited(
                queryset, self.DELIMITED_FORMATS[output_format])
        else:
            raise CommandError(
                "Unsupported format '%s'; choose from: %s"
                % (output_format, ", ".join(self.supported_formats())))
