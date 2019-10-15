from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django_boost.admin.sites import register_all
from django_boost.forms import UserCreationForm
from django_boost.models import EmailUser

__all__ = ["EmailUserAdmin", "register_all"]


@admin.register(EmailUser)
class EmailUserAdmin(UserAdmin):
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
