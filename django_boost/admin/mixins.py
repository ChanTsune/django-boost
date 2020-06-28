from .actions import hard_delete_selected
from .filters import LogicalDeletedFilter


class LogicalDeletionModelAdminMixin:

    def hard_delete_queryset(self, request, queryset):
        queryset.delete(hard=True)

    def get_actions(self, request):
        self.admin_site.add_action(hard_delete_selected)
        return super().get_actions(request)

    def get_list_filter(self, request):
        filters = super().get_list_filter(request)
        filters = list(filters) + [LogicalDeletedFilter]
        return filters
