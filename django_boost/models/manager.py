from django.db.models.manager import Manager

from django_boost.models.query import LogicalDeletionQuerySet


class LogicalDeletionManager(Manager):
    delete_flag_field = "deleted_at"

    def get_deleted_flag_field_name(self):
        return self.delete_flag_field

    def get_queryset(self):
        return LogicalDeletionQuerySet(self.model)

    def delete(self, hard=False):
        return self.get_queryset().delete(hard=hard)

    def alive(self):
        return self.get_queryset().alive()

    def dead(self):
        return self.get_queryset().dead()
