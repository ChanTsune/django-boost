"""Extensions for Django's ``django.db.models.query``."""

from __future__ import annotations

import datetime

import django
from django.db.models.query import QuerySet
from django.utils import timezone

from django_boost.models.deletion import LogicalDeletionCollector


class LogicalDeletionQuerySet(QuerySet):
    """QuerySet for ``LogicalDeletionMixin``; ``delete()`` marks rows dead instead of removing them."""

    delete_flag_field = "deleted_at"

    def get_delete_flag_field_name(self):  # noqa: D102
        return self.delete_flag_field

    def _clone(self):
        # delete_flag_field is set as an instance attribute by the manager, but
        # QuerySet._clone() only copies a fixed set of attributes, so carry it
        # forward or a chained alive()/dead()/revive() would fall back to the
        # class default and query the wrong column.
        clone = super()._clone()
        clone.delete_flag_field = self.delete_flag_field
        return clone

    def delete(self, hard=False, deleted_at=None):
        """Mark matched rows dead, or physically delete them when ``hard=True``."""
        if hard:
            return super().delete()
        if hasattr(self, '_not_support_combined_queries'):
            self._not_support_combined_queries('delete')
        if self.query.is_sliced:
            raise TypeError("Cannot use 'limit' or 'offset' with delete().")
        # Match Django's per-version guard: <5.0 rejects any .distinct(); 5.0+
        # rejects only .distinct(*fields).
        if django.VERSION >= (5, 0):
            if self.query.distinct_fields:
                raise TypeError("Cannot call delete() after .distinct(*fields).")
        elif self.query.distinct or self.query.distinct_fields:
            raise TypeError("Cannot call delete() after .distinct().")
        if getattr(self, '_fields', None) is not None:
            raise TypeError("Cannot call delete() after .values() or .values_list()")

        del_query = self._chain()
        del_query._for_write = True
        del_query.query.select_for_update = False
        del_query.query.select_related = False
        del_query.query.clear_ordering(force=True)

        collector = LogicalDeletionCollector(
            using=del_query.db, origin=self, deleted_at=deleted_at)
        collector.collect(del_query)
        deleted, rows_count = collector.delete()

        self._result_cache = None
        return deleted, rows_count

    delete.alters_data = True
    delete.queryset_only = True

    def alive(self):  # noqa: D102
        field_name = self.get_delete_flag_field_name()
        return self.filter(**{field_name: None})

    def dead(self):  # noqa: D102
        field_name = self.get_delete_flag_field_name()
        return self.exclude(**{field_name: None})

    def revive(self):
        """Revive logical delete items."""
        field_name = self.get_delete_flag_field_name()
        return self.update(**{field_name: None})

    revive.alters_data = True
    revive.queryset_only = True

    def _filter_delete_flag(self, gte=None, lt=None):
        field_name = self.get_delete_flag_field_name()
        lookups = {}
        if gte is not None:
            lookups[f'{field_name}__gte'] = gte
        if lt is not None:
            lookups[f'{field_name}__lt'] = lt
        return self.filter(**lookups)

    def deleted_since(self, days):
        """Return items whose delete flag falls within the past ``days`` calendar days, today inclusive."""
        today = self._local_today()
        since = today - datetime.timedelta(days=days - 1)
        tomorrow = today + datetime.timedelta(days=1)
        return self._filter_delete_flag(
            gte=self._local_day_start(since), lt=self._local_day_start(tomorrow))

    def deleted_before(self, date):
        """Return items whose delete flag is strictly before the local start of ``date``."""
        return self._filter_delete_flag(lt=self._local_day_start(self._as_date(date)))

    def deleted_between(self, start=None, end=None):
        """Return items whose delete flag falls within the inclusive local-calendar-day range ``[start, end]``."""
        gte = self._local_day_start(self._as_date(start)) if start is not None else None
        lt = None
        if end is not None:
            lt = self._local_day_start(self._as_date(end) + datetime.timedelta(days=1))
        return self._filter_delete_flag(gte=gte, lt=lt)

    @staticmethod
    def _as_date(value):
        if isinstance(value, datetime.datetime):
            if timezone.is_aware(value):
                value = timezone.localtime(value)
            return value.date()
        return value

    @staticmethod
    def _local_today():
        now = timezone.now()
        if timezone.is_aware(now):
            now = timezone.localtime(now)
        return now.date()

    @staticmethod
    def _local_day_start(date):
        start = datetime.datetime.combine(date, datetime.time.min)
        if timezone.is_aware(timezone.now()):
            start = timezone.make_aware(start)
        return start
