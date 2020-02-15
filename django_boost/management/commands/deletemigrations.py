import os

from django.utils.translation import gettext as _

from django_boost.core.management import AppCommand


class Command(AppCommand):
    help = "delete migration files."

    def confirm(self):
        if not self.yes:
            answer = None
            while not answer or answer not in "yn":
                answer = input(_("Do you wish to delete? [y/N] "))
                if not answer:
                    answer = "n"
                    break
                else:
                    answer = answer[0].lower()
            return answer == "y"
        return True

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('-y', action='store_true')

    def handle_app_config(self, app_config, **options):
        self.yes = options['y']
        app_path = app_config.path
        migration_dir = os.path.join(app_path, 'migrations')
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
        if self.confirm():
            for file in file_list:
                os.remove(file)
            self.stdout.write(self.style.SUCCESS('file deleted.'))
        else:
            self.stderr.write('job canceled.')

