from __future__ import annotations

from typing import Any

from django.conf import settings
from django.db import DEFAULT_DB_ALIAS
from django.db.models import Model


class DatabaseRouter:
    """Route Django apps to database aliases from DATABASE_APPS_MAPPING."""

    def __init__(self) -> None:
        """Load the app-to-database mapping from ``settings.DATABASE_APPS_MAPPING``."""
        self.db_map: dict[str, str] = getattr(
            settings, "DATABASE_APPS_MAPPING", {})

    def db_for_read(self, model: type[Model], **hints: Any) -> str | None:
        return self.db_map.get(model._meta.app_label, None)

    def db_for_write(self, model: type[Model], **hints: Any) -> str | None:
        return self.db_map.get(model._meta.app_label, None)

    def allow_relation(self, obj1: Model, obj2: Model, **hints: Any) -> bool | None:
        db1 = self.db_map.get(obj1._meta.app_label)
        db2 = self.db_map.get(obj2._meta.app_label)
        if db1 and db2:
            return db1 == db2
        return None

    def allow_migrate(self, db: str, app_label: str, model: Any = None,
                      **hints: Any) -> bool | None:
        if app_label in self.db_map:
            return self.db_map[app_label] == db
        if db != DEFAULT_DB_ALIAS and db in self.db_map.values():
            return False
        return None
