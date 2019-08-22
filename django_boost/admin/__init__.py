from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django_boost.models import EmailUser
# Register your models here.


@admin.register(EmailUser)
class EmailUserAdmin(UserAdmin):
    pass
