from django.contrib import admin
from django.db.models import Model

__all__ = ["register_all"]


def register_all(models, admin_class=admin.ModelAdmin):
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
    for attr in dir(models):
        attr = getattr(models, attr, None)
        if isinstance(attr, type):
            if issubclass(attr, Model) and not attr._meta.abstract:
                try:
                    admin.site.register(attr, admin_class)
                except admin.sites.AlreadyRegistered:
                    pass
