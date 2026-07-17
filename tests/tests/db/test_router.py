import warnings
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase as UnitTestCase

from django.conf import settings
from django.core.management import call_command
from django.db import connections
from django.test import SimpleTestCase, override_settings

from django_boost.db.router import DatabaseRouter
from example.models import Customer


def clear_router_test_connection(alias):
    connection = getattr(connections._connections, alias, None)
    if connection is not None:
        connection.close()
        delattr(connections._connections, alias)
    connections.databases.pop(alias, None)


class DatabaseRouterAllowMigrateTests(SimpleTestCase):

    @override_settings(DATABASE_APPS_MAPPING={'shop': 'default'})
    def test_unmapped_app_is_not_blocked_on_default(self):
        # An app mapped to 'default' must not stop unmapped apps (auth,
        # sessions, ...) from migrating there. Defer with None, not False.
        router = DatabaseRouter()
        self.assertIsNone(router.allow_migrate('default', 'auth'))

    @override_settings(DATABASE_APPS_MAPPING={'shop': 'shopdb'})
    def test_mapped_app_is_confined_to_its_database(self):
        router = DatabaseRouter()
        self.assertTrue(router.allow_migrate('shopdb', 'shop'))
        self.assertFalse(router.allow_migrate('default', 'shop'))

    @override_settings(DATABASE_APPS_MAPPING={'shop': 'shopdb'})
    def test_unmapped_app_is_blocked_on_mapped_non_default_database(self):
        router = DatabaseRouter()
        self.assertIsNone(router.allow_migrate('default', 'auth'))
        self.assertFalse(router.allow_migrate('shopdb', 'auth'))

    @override_settings(DATABASE_APPS_MAPPING={'shop': 'shopdb'})
    def test_unmapped_app_defers_on_unmapped_non_default_database(self):
        # A non-default database that no app maps to is none of the router's
        # business: defer so unmapped apps can still migrate onto it.
        router = DatabaseRouter()
        self.assertIsNone(router.allow_migrate('otherdb', 'auth'))


class DatabaseRouterDynamicMappingTests(SimpleTestCase):

    def test_mapping_change_is_picked_up_by_an_already_constructed_router(self):
        # The router instance predates the override, so this only passes if
        # DATABASE_APPS_MAPPING is read fresh on each call rather than
        # snapshotted at construction time.
        router = DatabaseRouter()
        with override_settings(DATABASE_APPS_MAPPING={'shop': 'shopdb'}):
            self.assertTrue(router.allow_migrate('shopdb', 'shop'))
            self.assertFalse(router.allow_migrate('default', 'shop'))

    def test_mapping_seen_inside_override_does_not_leak_after_it_exits(self):
        with override_settings(DATABASE_APPS_MAPPING={'shop': 'shopdb'}):
            router = DatabaseRouter()
            self.assertTrue(router.allow_migrate('shopdb', 'shop'))
        # Back on the process-wide setting: the mapping seen during
        # construction must not persist on the router past the override.
        self.assertIsNone(router.allow_migrate('shopdb', 'shop'))
        self.assertTrue(router.allow_migrate('example', 'example'))


class DatabaseRouterConfiguredExampleTests(SimpleTestCase):

    def test_example_app_routes_to_configured_example_database(self):
        router = DatabaseRouter()
        self.assertEqual(router.db_for_read(Customer), 'example')
        self.assertEqual(router.db_for_write(Customer), 'example')
        self.assertTrue(router.allow_migrate('example', 'example'))
        self.assertFalse(router.allow_migrate('default', 'example'))
        self.assertFalse(router.allow_migrate('example', 'contenttypes'))


class DatabaseRouterMigrationTests(UnitTestCase):

    def test_migrate_keeps_unmapped_apps_off_a_mapped_database(self):
        # End-to-end check that the router is wired into migrate, not just
        # exercised in isolation like the unit tests above. django_content_type
        # is the negative control because contenttypes is installed and would
        # migrate here if the router allowed it (unlike auth_user, which
        # AUTH_USER_MODEL swaps out regardless of the router). The
        # 'default'-database regression is covered by those unit tests; migrate
        # cannot exercise it without replacing the test runner's own 'default'
        # connection.
        alias = 'router_test'
        tmpdir = TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)

        databases = dict(settings.DATABASES)
        databases[alias] = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(Path(tmpdir.name) / 'router-test.sqlite3'),
        }
        with warnings.catch_warnings():
            warnings.filterwarnings(
                'ignore',
                message=r'Overriding setting DATABASES can lead to unexpected behavior\.',
                category=UserWarning,
            )
            with override_settings(
                DATABASES=databases,
                DATABASE_ROUTERS=['django_boost.db.router.DatabaseRouter'],
                DATABASE_APPS_MAPPING={'sessions': alias},
            ):
                connections.databases[alias] = connections.configure_settings(databases)[alias]
                self.addCleanup(clear_router_test_connection, alias)
                connection = connections[alias]
                call_command('migrate', database=alias, verbosity=0, interactive=False)
                tables = set(connection.introspection.table_names())

        self.assertIn('django_session', tables)
        self.assertNotIn('django_content_type', tables)
