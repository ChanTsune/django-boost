"""Guard against dropping the historical EmailUser database table."""

from importlib import import_module

from django.db.migrations import SeparateDatabaseAndState
from django.db.migrations.loader import MigrationLoader
from django.test import SimpleTestCase

import django_boost.models as boost_models
import django_boost.admin as boost_admin


class RemovedEmailUserTests(SimpleTestCase):
    def test_legacy_user_models_and_admin_are_removed(self):
        self.assertFalse(hasattr(boost_models, "EmailUser"))
        self.assertFalse(hasattr(boost_models, "AbstractEmailUser"))
        self.assertFalse(hasattr(boost_admin, "EmailUserAdmin"))

    def test_state_only_migration_preserves_existing_table(self):
        module = import_module("django_boost.migrations.0004_remove_emailuser_state")
        self.assertEqual(len(module.Migration.operations), 1)
        operation = module.Migration.operations[0]
        self.assertIsInstance(operation, SeparateDatabaseAndState)
        self.assertEqual(operation.database_operations, [])
        state = MigrationLoader(None).project_state()
        self.assertNotIn(("django_boost", "emailuser"), state.models)
