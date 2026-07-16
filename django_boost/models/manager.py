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

    def deleted_since(self, days):
        """Return items whose delete flag falls within the past ``days`` calendar days, today inclusive."""
        return self.get_queryset().deleted_since(days)

    def deleted_before(self, date):
        """Return items whose delete flag is strictly before the local start of ``date``."""
        return self.get_queryset().deleted_before(date)

    def deleted_between(self, start=None, end=None):
        """Return items whose delete flag falls within the inclusive local-calendar-day range ``[start, end]``.

        Either bound may be omitted to leave that side of the range open;
        with both omitted, all logically deleted items are returned.
        """
        return self.get_queryset().deleted_between(start=start, end=end)

    def revive(self):
        """Revive logical deleted items."""
        return self.get_queryset().revive()

    revive.alters_data = True
