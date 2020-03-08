import sys
from os import path
from platform import python_version
try:
    from pip._internal.commands import freeze
except ImportError:
    try:
        from pip._internal.operations import freeze
    except ImportError:  # pip < 10.0
        from pip.operations import freeze

from django.conf import settings

from django_boost.core.management import BaseCommand


def _make_all(runtime, prockfile, requirments, **_):
    return not any([runtime, prockfile, requirments])


class Command(BaseCommand):
    """Create a configuration file for heroku."""

    help = "Create a configuration file for heroku" + \
        "\n`Procfile`,`runtime.txt` and `requirements.txt`\n"
    PROCFILE = "Procfile"
    PROCFILE_WEB = "web: gunicorn %s\n"
    PROCFILE_RELEASE = "release: %s\n"
    RUNTIME = "runtime.txt"
    RUNTIME_FORMAT = "python-%s\n"
    REQUIREMENTS = "requirements.txt"

    GUNICORN = 'gunicorn'

    def add_arguments(self, parser):
        parser.add_argument('--overwrite', action='store_true',
                            help='Overwrite even if file exists.')
        parser.add_argument('--no-gunicorn', action='store_true',
                            help="Don't automatically add `gunicorn` "
                            "to `requirements.txt`.")
        parser.add_argument('--runtime', action='store_true',
                            help='Create only `runtime.txt`'
                            ', By default all files are created.')
        parser.add_argument('--prockfile', action='store_true',
                            help='Create  only `Prockfile`'
                            ', By default all files are created.')
        parser.add_argument('--release', nargs='+', default=[],
                            help='Add the command to be executed '
                            'in the release phase to `Prockfile`')
        parser.add_argument('--requirments', action='store_true',
                            help='Create  only `requirments.txt`'
                            ', By default all files are created.')
        parser.add_argument('-q', '--quit', action='store_true',
                            help="Don't output to standard output.")

    def handle(self, *args, **options):
        EXEC_PATH = sys.argv[0]
        ROOT_DIR = path.dirname(path.abspath(EXEC_PATH))
        make_all = _make_all(**options)
        if make_all or options['prockfile']:
            PROCFILE_PATH = path.join(ROOT_DIR, self.PROCFILE)
            self.make_prockfile(PROCFILE_PATH, **options)
        if make_all or options['runtime']:
            RUNTIME_PATH = path.join(ROOT_DIR, self.RUNTIME)
            self.make_runtime(RUNTIME_PATH, **options)
        if make_all or options['requirments']:
            REQUIREMENTS_PATH = path.join(ROOT_DIR, self.REQUIREMENTS)
            self.make_requirments(REQUIREMENTS_PATH, **options)

    def _print_generated_path(self, path, quit, **options):
        if not quit:
            self.stdout.write("Generated : " + path)

    def make_runtime(self, fpath, **options):
        if not path.exists(fpath) or options['overwrite']:
            with open(fpath, "w") as f:
                f.write(self.RUNTIME_FORMAT % python_version())
            self._print_generated_path(fpath, **options)

    def make_prockfile(self, fpath, **options):
        wsgi = ".".join(settings.WSGI_APPLICATION.split(".")[:-1])
        if not path.exists(fpath) or options['overwrite']:
            with open(fpath, "w") as f:
                for release in options['release']:
                    f.write(self.PROCFILE_RELEASE % release)
                f.write(self.PROCFILE_WEB % wsgi)
            self._print_generated_path(fpath, **options)

    def make_requirments(self, fpath, no_gunicorn, **options):
        gunicorn_exist = False
        if not path.exists(fpath) or options['overwrite']:
            with open(fpath, "w") as f:
                for i in freeze.freeze():
                    if i.startswith(self.GUNICORN):
                        gunicorn_exist = True
                    f.write(i)
                    f.write('\n')
                if not gunicorn_exist and not no_gunicorn:
                    f.write(self.GUNICORN)
                    f.write('\n')
            self._print_generated_path(fpath, **options)
