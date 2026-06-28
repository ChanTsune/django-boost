from __future__ import annotations

from django.db.models.manager import Manager

from .query import LogicalDeletionQuerySet


class LogicalDeletionManager(Manager):
    delete_flag_field = "deleted_at"

    def get_deleted_flag_field_name(self):
        return self.delete_flag_field

    def get_queryset(self):
        qs = LogicalDeletionQuerySet(self.model, using=self._db, hints=self._hints)
        qs.delete_flag_field = self.get_deleted_flag_field_name()
        return qs

    def delete(self, hard=False, deleted_at=None):
        return self.get_queryset().delete(hard=hard, deleted_at=deleted_at)

    def alive(self):
        """Return not logically deleted items queryset."""
        return self.get_queryset().alive()

    def dead(self):
        """Return logically deleted items queryset."""
        return self.get_queryset().dead()

    def revive(self):
        """Revive logical deleted items."""
        return self.get_queryset().revive()
