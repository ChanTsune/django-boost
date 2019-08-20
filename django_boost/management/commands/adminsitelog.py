from django.core.management import BaseCommand
from django.contrib.admin.models import LogEntry
from django.utils.translation import gettext_lazy as _

from django_boost.core import get_version


class Command(BaseCommand):

    def print_log(self, log):
        fmt = "{id} | {action} | {object} | {user} | {time}"
        fmap = {}
        if log.is_addition():
            fmap["action"] = self.style.SUCCESS("Added")
            fmap["object"] = log.object_repr
        elif log.is_change():
            fmap["action"] = self.style.WARNING("Changed")
            fmap["object"] = "%s - %s" % (log.object_repr,
                                          log.get_change_message())
        else:  # log.is_deletion
            fmap["action"] = self.style.ERROR("Deleted")
            fmap["object"] = log.object_repr
        fmap["user"] = log.user.username
        fmap["time"] = log.action_time
        fmap["id"] = log.id
        self.stdout.write(fmt.format_map(fmap))

    def add_arguments(self, parser):
        parser.add_argument('-d', '--delete', action='store_true')
        parser.add_argument('--filter', nargs="+", type=str, default=[])
        parser.add_argument('--exclude', nargs="+", type=str, default=[])
        parser.add_argument('--order_by', nargs="+",
                            type=str, default=["action_time"])

    def handle(self, *args, **options):
        self.stdout.write(str(args))
        self.stdout.write(str(options))
        queryset = LogEntry.objects.all()
        queryset = queryset.order_by(*options['order_by'])
        if queryset.count() == 0:
            self.stderr.write('No logs')
            return
        for log in queryset:
            self.print_log(log)
        if options['delete']:
            answer = input(_("Do you want to delete these logs [y/n]?"))
            if answer.lower() in ["y", "yes"]:
                queryset.delete()
                self.stdout.write('delete complete')
            else:
                self.stderr.write('operation canceled')
            return

    def get_version(self):
        return get_version()
