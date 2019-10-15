from django.contrib import admin
from django.db.models import Model

__all__ = ["register_all"]


def register_all(models, admin_class=admin.ModelAdmin):
    for attr in dir(models):
        attr = getattr(models, attr, None)
        if isinstance(attr, type):
            if issubclass(attr, Model) and not attr._meta.abstract:
                try:
                    admin.site.register(attr, admin_class)
                except admin.sites.AlreadyRegistered:
                    pass
