from __future__ import annotations

from django.conf import settings
from django.db import DEFAULT_DB_ALIAS


class DatabaseRouter:
    """Route Django apps to database aliases from DATABASE_APPS_MAPPING."""

    def __init__(self):
        self.db_map = getattr(settings, "DATABASE_APPS_MAPPING", {})

    def db_for_read(self, model, **hints):
        return self.db_map.get(model._meta.app_label, None)

    def db_for_write(self, model, **hints):
        return self.db_map.get(model._meta.app_label, None)

    def allow_relation(self, obj1, obj2, **hints):
        db1 = self.db_map.get(obj1._meta.app_label)
        db2 = self.db_map.get(obj2._meta.app_label)
        if db1 and db2:
            return db1 == db2
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        if app_label in self.db_map:
            return self.db_map[app_label] == db
        if db != DEFAULT_DB_ALIAS and db in self.db_map.values():
            return False
        return None
