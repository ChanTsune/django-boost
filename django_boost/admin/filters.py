"""Admin list filters for Django's ``django.contrib.admin``."""

from __future__ import annotations

from django.contrib import admin


class LogicalDeletedFilter(admin.SimpleListFilter):
    """Admin list filter for alive/dead items on a ``LogicalDeletionMixin`` model."""

    title = 'delete state'
    parameter_name = 'delete_state'

    def lookups(self, request, model_admin):  # noqa: D102
        return (
            ('alive', ('Alive')),
            ('dead', ('Dead')),
        )

    def queryset(self, request, queryset):  # noqa: D102
        value = self.value()
        if value == 'alive':
            return queryset.alive()
        if value == 'dead':
            return queryset.dead()
