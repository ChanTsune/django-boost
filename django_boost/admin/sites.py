from inspect import getmembers, isclass

from django.contrib import admin
from django.db.models.base import ModelBase

__all__ = ["register_all"]


def register_all(models, admin_class=admin.ModelAdmin, **options):
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
        if issubclass(klass, ModelBase) and not klass._meta.abstract:
            try:
                admin.site.register(klass, admin_class, **options)
            except admin.sites.AlreadyRegistered:
                pass
