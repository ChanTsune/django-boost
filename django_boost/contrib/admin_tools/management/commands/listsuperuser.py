"""The ``listsuperuser`` management command."""

from __future__ import annotations

from typing import Any, cast

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.management.base import CommandParser
from django.db.models import QuerySet

from django_boost.core.management import BaseCommand
from django_boost.management.mixins import OutputFormatMixin


class Command(OutputFormatMixin, BaseCommand):
    """List super users with audit-relevant fields."""

    help = "List super users."
    OUTPUT_FIELDS = ("email", "active", "staff", "last_login")

    def add_arguments(self, parser: CommandParser) -> None:  # noqa: D102
        self.add_format_option(parser)

    def get_queryset(self) -> QuerySet[AbstractUser]:  # noqa: D102
        # get_user_model() is only guaranteed to be AbstractBaseUser, but
        # listing superusers inherently needs is_staff/is_superuser/
        # USERNAME_FIELD, which live on AbstractUser (via PermissionsMixin).
        User = cast(type[AbstractUser], get_user_model())
        return User.objects.filter(
            is_superuser=True).order_by(User.USERNAME_FIELD)

    def get_row_data(self, obj: AbstractUser, **options: Any) -> dict[str, str]:  # noqa: D102
        email_field = obj.get_email_field_name()
        return {
            "email": getattr(obj, email_field, "") or "",
            "active": "yes" if obj.is_active else "no",
            "staff": "yes" if obj.is_staff else "no",
            "last_login": str(obj.last_login) if obj.last_login else "(never)",
        }

    def handle(self, *args: Any, **options: Any) -> None:  # noqa: D102
        self.print_formatted(self.get_queryset(), **options)
