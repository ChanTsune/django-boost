from django.contrib import admin


class LogicalDeletedFilter(admin.SimpleListFilter):
    title = 'delete state'
    parameter_name = 'delete_state'

    def lookups(self, request, model_admin):
        return (
            ('alive', ('Alive')),
            ('dead', ('Dead')),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'alive':
            return queryset.alive()
        if value == 'dead':
            return queryset.dead()
