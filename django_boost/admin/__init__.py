"""Admin site extensions for Django's ``django.contrib.admin``."""

from __future__ import annotations

from django.contrib import admin


from .filters import LogicalDeletedDateFilter
from .mixins import LogicalDeletionModelAdminMixin
from .sites import register_all

__all__ = ["LogicalDeletedDateFilter",
           "LogicalDeletionModelAdmin",
           "register_all"]


class LogicalDeletionModelAdmin(LogicalDeletionModelAdminMixin, admin.ModelAdmin):
    """ModelAdmin for Model that inherited LogicalDeletionModelMixin."""
