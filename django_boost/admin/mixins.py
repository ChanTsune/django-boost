from __future__ import annotations

from .actions import hard_delete_selected
from .filters import LogicalDeletedFilter


class LogicalDeletionModelAdminMixin:

    def hard_delete_queryset(self, request, queryset):
        queryset.delete(hard=True)

    def get_actions(self, request):
        # Add the action to this admin's own action set only; add_action()
        # would register it on the shared AdminSite and leak it to every
        # other model admin.
        actions = super().get_actions(request)
        if actions and self.has_delete_permission(request):
            func, name, description = self.get_action(hard_delete_selected)
            actions[name] = (func, name, description)
        return actions

    def get_list_filter(self, request):
        filters = super().get_list_filter(request)
        filters = list(filters) + [LogicalDeletedFilter]
        return filters
