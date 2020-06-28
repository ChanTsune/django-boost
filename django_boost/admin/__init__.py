from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django_boost.forms import UserCreationForm
from django_boost.models import EmailUser

from .mixins import LogicalDeletionModelAdminMixin
from .sites import register_all

__all__ = ["EmailUserAdmin",
           "LogicalDeletionModelAdmin",
           "register_all"]


@admin.register(EmailUser)
class EmailUserAdmin(UserAdmin):
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


class LogicalDeletionModelAdmin(LogicalDeletionModelAdminMixin, admin.ModelAdmin):
    """ModelAdmin for Model that inherited LogicalDeletionModelMixin."""
