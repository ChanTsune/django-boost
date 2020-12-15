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

    def handle_app_config(self, app_config, **options):
        self.if_needed_make_quit(**options)
        app_path = app_config.path
        migration_dir = os.path.join(app_path, MIGRATIONS_MODULE_NAME)
        file_list = []
        if os.path.exists(migration_dir):
            for d, dirs, files in os.walk(migration_dir):
                for file in files:
                    if file == '__init__.py' or not file.endswith('.py'):
                        continue
                    self.stdout.write(file)
                    file_list.append(os.path.join(d, file))
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
