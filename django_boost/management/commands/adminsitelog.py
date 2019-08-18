from django.core.management import BaseCommand
from django.contrib.admin.models import LogEntry
from django.utils.translation import gettext_lazy as _

from django_boost.core import get_version


class Command(BaseCommand):

    def print_log(self,log):
        self.stdout.write(str(log))

    def add_arguments(self, parser):
        parser.add_argument('-d', '--delete', action='store_true')
        parser.add_argument('--username', nargs="+", type=str, default=None)

    def handle(self, *args, **options):
        self.stdout.write(str(args))
        self.stdout.write(str(options))
        queryset = LogEntry.objects.all()
        if options['username']:
            queryset = queryset.filter(user__username__in=options['username'])
        if queryset.count() == 0:
            self.stderr.write('No logs')
            return
        for log in queryset:
            self.print_log(log)
        if options['delete']:
            answer = input(_("Do you want to delete these logs [y/n]?"))
            if answer.lower() in ["y","yes"]:
                queryset.delete()
                self.stdout.write('delete complete')
            else:
                self.stderr.write('operation canceled')
            return
        from pprint import pprint
        pprint(dir(LogEntry))


    def get_version(self):
        return get_version()
