"""The ``migrate_emailuser`` management command."""

from __future__ import annotations

from django.apps import apps
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.recorder import MigrationRecorder

from django_boost.core.management import BaseCommand

LEGACY_TABLE = "django_boost_emailuser"
LEGACY_APP_LABEL = "django_boost"
LEGACY_MODEL = "emailuser"
LEGACY_USER_MODEL = "django_boost.EmailUser"


def adopt_content_type(using, from_label, from_model, to_label, to_model) -> int:
    """Rename the legacy ContentType in place so its permissions carry over.

    Returns the number of rows updated (0 if nothing to adopt).
    """
    if not apps.is_installed("django.contrib.contenttypes"):
        return 0
    from django.contrib.contenttypes.models import ContentType
    content_types = ContentType.objects.using(using)
    if content_types.filter(app_label=to_label, model=to_model).exists():
        return 0
    return content_types.filter(app_label=from_label, model=from_model).update(
        app_label=to_label, model=to_model)


def record_migration_applied(using, app_label, name) -> bool:
    """Record a migration as applied without running it. Idempotent.

    Returns True if a new record was written, False if it was already present.
    """
    recorder = MigrationRecorder(connections[using])
    recorder.ensure_schema()
    if (app_label, name) in recorder.applied_migrations():
        return False
    recorder.record_applied(app_label, name)
    return True


class Command(BaseCommand):  # noqa: D101
    help = ("Adopt the legacy django_boost_emailuser table and content type into your own "
            "AUTH_USER_MODEL app, then finish migrating.")

    def add_arguments(self, parser):
        parser.add_argument("--database", default=DEFAULT_DB_ALIAS)
        parser.add_argument(
            "--target-migration", default="0001_initial",
            help="Migration in the target app that creates the user model "
                 "(default: 0001_initial).")

    def handle(self, *args, **options):
        using = options["database"]
        target = getattr(settings, "AUTH_USER_MODEL", "") or ""
        if target == LEGACY_USER_MODEL or "." not in target:
            raise CommandError(
                "Set AUTH_USER_MODEL to your own model (e.g. 'accounts.User') before running "
                "migrate_emailuser; it must not be '%s'." % LEGACY_USER_MODEL)

        target_app, target_model = target.split(".", 1)
        model_name = target_model.lower()

        adopted = adopt_content_type(
            using, LEGACY_APP_LABEL, LEGACY_MODEL, target_app, model_name)
        if adopted:
            self.stdout.write(
                "Adopted content type %s.%s -> %s.%s (permissions preserved)."
                % (LEGACY_APP_LABEL, LEGACY_MODEL, target_app, model_name))

        if LEGACY_TABLE in connections[using].introspection.table_names():
            migration = options["target_migration"]
            if record_migration_applied(using, target_app, migration):
                self.stdout.write(
                    "Recorded %s.%s as applied (existing %s adopted)."
                    % (target_app, migration, LEGACY_TABLE))

        call_command("migrate", database=using)
        self.stdout.write(self.style.SUCCESS("migrate_emailuser complete."))
