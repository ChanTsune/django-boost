Admin Site Utilities
====================

:synopsis: Admin site utilities in django-boost


.. autofunction:: django_boost.admin.sites.register_all


Logical deletion admin
----------------------

Use :class:`django_boost.admin.LogicalDeletionModelAdmin` for a model based on
:class:`django_boost.models.LogicalDeletionMixin`::

    from django.contrib import admin
    from django_boost.admin import LogicalDeletionModelAdmin

    from .models import Article


    @admin.register(Article)
    class ArticleAdmin(LogicalDeletionModelAdmin):
        pass

The change list includes filters for alive/deleted state and deletion date.
The deletion-date filter offers all deleted items, today, the past 7, 30, or
90 calendar days, items older than 90 days, and an inclusive custom date
range. Date boundaries use Django's current time zone.
