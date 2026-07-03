from __future__ import annotations

import os

from django.db.migrations.loader import MIGRATIONS_MODULE_NAME
from django.utils.translation import gettext as _

from django_boost.core.management import AppCommand
from django_boost.management.mixins import ConfirmOptionMixin, QuitOptionMixin


class Command(ConfirmOptionMixin, QuitOptionMixin, AppCommand):
    help = "delete migration files."

    def add_arguments(self, parser):
        super().add_arguments(parser)
        self.add_quit_option(parser)
        self.add_confirm_option(parser)

    @staticmethod
    def _migration_files(migration_dir):
        # Only the top-level migration modules; do not descend into nested
        # packages (e.g. a migrations/helpers/ holding non-migration modules),
        # which os.walk would sweep in and delete.
        file_list = []
        for name in sorted(os.listdir(migration_dir)):
            path = os.path.join(migration_dir, name)
            if not os.path.isfile(path):
                continue
            if name == '__init__.py' or not name.endswith('.py'):
                continue
            file_list.append(path)
        return file_list

    def handle_app_config(self, app_config, **options):
        self.if_needed_make_quit(**options)
        app_path = app_config.path
        migration_dir = os.path.join(app_path, MIGRATIONS_MODULE_NAME)
        file_list = []
        if os.path.exists(migration_dir):
            file_list = self._migration_files(migration_dir)
            for file in file_list:
                self.stdout.write(os.path.basename(file))
        if not file_list:
            self.stderr.write(
                'No migration files detected in %s' % app_config.name)
            return
        if self.confirm(message=_("Do you wish to delete?"), **options):
            for file in file_list:
                os.remove(file)
            self.stdout.write(self.style.SUCCESS('file deleted.'))
        else:
            self.stderr.write('job canceled.')
