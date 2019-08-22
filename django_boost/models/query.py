from django.db.models.query import QuerySet
from django.utils.timezone import now


class LogicalDeletionQuerySet(QuerySet):
    delete_flag_field = "deleted_at"

    def get_delete_flag_field_name(self):
        return self.delete_flag_field

    def delete(self, hard=False):
        if hard:
            return super().delete()
        field_name = self.get_delete_flag_field_name()
        return super().update(**{field_name: now()})

    def alive(self):
        field_name = self.get_delete_flag_field_name()
        return self.filter(**{field_name: None})

    def dead(self):
        field_name = self.get_delete_flag_field_name()
        return self.exclude(**{field_name: None})
