import os
import tempfile

from django.core.management import call_command

from django_boost.management.commands.deletemigrations import Command
from django_boost.test import TestCase


class TestDeleteMigrations(TestCase):

    def test_call_command(self):
       call_command('deletemigrations', 'tests')

    def test_only_top_level_migration_files_are_collected(self):
        with tempfile.TemporaryDirectory() as migration_dir:
            open(os.path.join(migration_dir, '__init__.py'), 'w').close()
            open(os.path.join(migration_dir, '0001_initial.py'), 'w').close()
            sub = os.path.join(migration_dir, 'helpers')
            os.mkdir(sub)
            open(os.path.join(sub, '__init__.py'), 'w').close()
            open(os.path.join(sub, 'util.py'), 'w').close()

            collected = Command._migration_files(migration_dir)

        names = sorted(os.path.basename(f) for f in collected)
        self.assertEqual(names, ['0001_initial.py'])
