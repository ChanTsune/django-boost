from django_boost.core.management import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    """Coverage"""

    help = "Coverage"

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--runserver', action='store_true')
        parser.add_argument('--url', action='store_true')


    def handle(self, *args, **options):
        from coverage.cmdline import main
        main(['run', "manage.py", "test"])
        main(['html'])
        if options['url']:
            self.stdout.write('')
        if options['runserver']:
            call_command('runserver')

