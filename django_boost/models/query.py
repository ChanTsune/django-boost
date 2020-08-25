from django.db.models.query import QuerySet


class LogicalDeletionQuerySet(QuerySet):
    delete_flag_field = "deleted_at"

    def get_delete_flag_field_name(self):
        return self.delete_flag_field

    def delete(self, hard=False):
        if hard:
            return super().delete()
        field_name = self.get_delete_flag_field_name()
        deleted_value = self.model.get_deleted_value()
        return super().update(**{field_name: deleted_value})

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
