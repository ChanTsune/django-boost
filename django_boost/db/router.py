from django.conf import settings


class DatabaseRouter:

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
        if db in self.db_map.values():
            return self.db_map.get(app_label) == db
        elif app_label in self.db_map:
            return False
