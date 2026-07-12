"""Extensions for Django's ``django.db.models.manager``."""

from __future__ import annotations

from django.db.models.manager import Manager

from .query import LogicalDeletionQuerySet


class LogicalDeletionManager(Manager):
    """Default manager for ``LogicalDeletionMixin`` models; ``delete()`` marks rows dead instead of removing them."""

    delete_flag_field = "deleted_at"

    def get_deleted_flag_field_name(self):  # noqa: D102
        return self.delete_flag_field

    def get_queryset(self):  # noqa: D102
        qs = LogicalDeletionQuerySet(self.model, using=self._db, hints=self._hints)
        qs.delete_flag_field = self.get_deleted_flag_field_name()
        return qs

    def delete(self, hard=False, deleted_at=None):  # noqa: D102
        return self.get_queryset().delete(hard=hard, deleted_at=deleted_at)

    delete.alters_data = True

    def alive(self):
        """Return not logically deleted items queryset."""
        return self.get_queryset().alive()

    def dead(self):
        """Return logically deleted items queryset."""
        return self.get_queryset().dead()

    def revive(self):
        """Revive logical deleted items."""
        return self.get_queryset().revive()

    revive.alters_data = True
