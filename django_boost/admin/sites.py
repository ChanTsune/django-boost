from django.contrib import admin
from django.db.models import Model


def register_all(models, admin_class=admin.ModelAdmin):
    for attr in dir(models):
        attr = getattr(models, attr, None)
        if isinstance(attr, type) and issubclass(attr, Model) and not attr._meta.abstract:
            admin.site.register(attr, admin_class)
