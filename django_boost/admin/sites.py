"""Admin site helpers for Django's ``django.contrib.admin``."""

from __future__ import annotations

from inspect import getmembers, isclass
from types import ModuleType
from typing import Any

from django.contrib import admin
# AlreadyRegistered moved from admin.sites to admin.exceptions in Django 5.0;
# admin.sites still re-exports it in every supported version (4.2-5.2), but
# django-stubs' sites.pyi never declares it there -- import runtime-safely
# and silence the resulting attr-defined error rather than importing from
# admin.exceptions, which doesn't exist on Django 4.2.
from django.contrib.admin.sites import AlreadyRegistered  # type: ignore[attr-defined]
from django.db.models.base import ModelBase

__all__ = ["register_all"]


def register_all(
    models: ModuleType,
    admin_class: type[admin.ModelAdmin] = admin.ModelAdmin,
    **options: Any,
) -> None:
    """
    Easily register Models to Django admin site.

    ::

      from yourapp import models
      from django_boost.admin.sites import register_all

      register_all(models)

      Register all models defined in `models.py` in Django admin site.

      Custom admin classes are also available.

    ::

      from your_app import models
      from your_app import admin
      from django_boost.admin.sites import register_all

      register_all(models, admin_class=admin.CustomAdmin)
    """
    for _, klass in getmembers(models, isclass):
        if isinstance(klass, ModelBase) and not klass._meta.abstract:
            try:
                admin.site.register(klass, admin_class, **options)
            except AlreadyRegistered:
                pass
