"""Admin mixins for Django's ``django.contrib.admin``."""

from __future__ import annotations

from .actions import hard_delete_selected
from .filters import LogicalDeletedDateFilter, LogicalDeletedFilter


class LogicalDeletionModelAdminMixin:
    """Mixin adding hard deletion and logical-deletion filters to a ``ModelAdmin``."""

    def hard_delete_queryset(self, request, queryset):  # noqa: D102
        queryset.delete(hard=True)

    def get_actions(self, request):  # noqa: D102
        # Add the action to this admin's own action set only; add_action()
        # would register it on the shared AdminSite and leak it to every
        # other model admin.
        actions = super().get_actions(request)
        if actions and self.has_delete_permission(request):
            func, name, description = self.get_action(hard_delete_selected)
            actions[name] = (func, name, description)
        return actions

    def get_list_filter(self, request):  # noqa: D102
        filters = super().get_list_filter(request)
        manager = self.model._default_manager
        get_field_name = getattr(manager, 'get_deleted_flag_field_name', None)
        field_name = get_field_name() if get_field_name else 'deleted_at'
        filters = list(filters) + [
            LogicalDeletedFilter,
            (field_name, LogicalDeletedDateFilter),
        ]
        return filters
