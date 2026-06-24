import django
from django.db.models.query import QuerySet

from django_boost.models.deletion import LogicalDeletionCollector


class LogicalDeletionQuerySet(QuerySet):
    delete_flag_field = "deleted_at"

    def get_delete_flag_field_name(self):
        return self.delete_flag_field

    def delete(self, hard=False, deleted_at=None):
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

    def alive(self):
        field_name = self.get_delete_flag_field_name()
        return self.filter(**{field_name: None})

    def dead(self):
        field_name = self.get_delete_flag_field_name()
        return self.exclude(**{field_name: None})

    def revive(self):
        """Revive logical delete items."""
        field_name = self.get_delete_flag_field_name()
        return self.update(**{field_name: None})
