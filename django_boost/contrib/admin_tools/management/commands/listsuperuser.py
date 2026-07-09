"""The ``listsuperuser`` management command."""

from __future__ import annotations

from django.contrib.auth import get_user_model

from django_boost.core.management import BaseCommand
from django_boost.management.mixins import OutputFormatMixin


class Command(OutputFormatMixin, BaseCommand):
    """List super users with audit-relevant fields."""

    help = "List super users."
    OUTPUT_FIELDS = ("email", "active", "staff", "last_login")

    def add_arguments(self, parser):
        self.add_format_option(parser)

    def get_queryset(self):
        User = get_user_model()
        return User.objects.filter(
            is_superuser=True).order_by(User.USERNAME_FIELD)

    def get_row_data(self, user, **options):
        email_field = user.get_email_field_name()
        return {
            "email": getattr(user, email_field, "") or "",
            "active": "yes" if user.is_active else "no",
            "staff": "yes" if user.is_staff else "no",
            "last_login": str(user.last_login) if user.last_login else "(never)",
        }

    def handle(self, *args, **options):
        self.print_formatted(self.get_queryset(), **options)
