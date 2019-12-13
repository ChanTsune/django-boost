from django.core.management import call_command

from django_boost.core.management import BaseCommand


class Command(BaseCommand):
    help = ""

    def add_arguments(self, parser):
        parser.add_argument('--remove', action='store_true')

    def handle(self, *args, **options):
        call_command('makemigrations', 'tests')
        call_command('test')
        if options['remove']:
            call_command('deletemigrations', 'tests', '-y')
