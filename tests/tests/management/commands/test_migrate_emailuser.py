from io import StringIO
from unittest.mock import Mock, patch

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.recorder import MigrationRecorder
from django.test import override_settings

from django_boost.management.commands.migrate_emailuser import (
    adopt_content_type,
    record_migration_applied,
)
from django_boost.test import TestCase


class AdoptContentTypeTests(TestCase):

    def test_moves_content_type_and_preserves_permissions(self):
        ct = ContentType.objects.create(app_label="django_boost", model="faketarget")
        perm = Permission.objects.create(
            content_type=ct, codename="add_faketarget", name="Can add faketarget")
        group = Group.objects.create(name="staff")
        group.permissions.add(perm)

        moved = adopt_content_type(
            DEFAULT_DB_ALIAS, "django_boost", "faketarget", "accounts", "faketarget")

        self.assertEqual(moved, 1)
        ct.refresh_from_db()
        self.assertEqual((ct.app_label, ct.model), ("accounts", "faketarget"))
        perm.refresh_from_db()
        self.assertEqual(perm.content_type_id, ct.id)
        self.assertIn(perm, group.permissions.all())

    def test_noop_when_target_already_exists(self):
        ContentType.objects.create(app_label="accounts", model="faketarget")
        ContentType.objects.create(app_label="django_boost", model="faketarget")
        moved = adopt_content_type(
            DEFAULT_DB_ALIAS, "django_boost", "faketarget", "accounts", "faketarget")
        self.assertEqual(moved, 0)


class RecordMigrationAppliedTests(TestCase):

    def test_is_idempotent(self):
        first = record_migration_applied(DEFAULT_DB_ALIAS, "accounts", "0001_initial")
        second = record_migration_applied(DEFAULT_DB_ALIAS, "accounts", "0001_initial")
        self.assertTrue(first)
        self.assertFalse(second)
        recorder = MigrationRecorder(connections[DEFAULT_DB_ALIAS])
        self.assertIn(("accounts", "0001_initial"), recorder.applied_migrations())


class MigrateEmailUserCommandTests(TestCase):

    @override_settings(AUTH_USER_MODEL="django_boost.EmailUser")
    def test_refuses_when_target_not_set(self):
        with self.assertRaisesRegex(CommandError, "AUTH_USER_MODEL"):
            call_command("migrate_emailuser", stdout=StringIO())

    @override_settings(AUTH_USER_MODEL="nouserdot")
    def test_refuses_when_target_has_no_dot(self):
        with self.assertRaisesRegex(CommandError, "AUTH_USER_MODEL"):
            call_command("migrate_emailuser", stdout=StringIO())

    @override_settings(AUTH_USER_MODEL="accounts.User")
    def test_adopts_and_records_before_migrate(self):
        module = "django_boost.management.commands.migrate_emailuser"
        manager = Mock()
        with patch(module + ".adopt_content_type", return_value=1) as adopt, \
                patch(module + ".record_migration_applied", return_value=True) as record, \
                patch(module + ".call_command") as migrate:
            manager.attach_mock(adopt, "adopt")
            manager.attach_mock(record, "record")
            manager.attach_mock(migrate, "migrate")
            call_command("migrate_emailuser", stdout=StringIO())

        adopt.assert_called_once_with(
            DEFAULT_DB_ALIAS, "django_boost", "emailuser", "accounts", "user")
        record.assert_called_once_with(DEFAULT_DB_ALIAS, "accounts", "0001_initial")
        migrate.assert_called_once_with("migrate", database=DEFAULT_DB_ALIAS)
        names = [c[0] for c in manager.mock_calls]
        self.assertLess(names.index("adopt"), names.index("migrate"))
        self.assertLess(names.index("record"), names.index("migrate"))
