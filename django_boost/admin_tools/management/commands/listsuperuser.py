"""Deprecated ``django_boost`` alias for ``contrib.admin_tools``'s ``listsuperuser`` command."""

from __future__ import annotations

from django_boost.contrib.admin_tools.management.commands.listsuperuser import (
    Command,
)

__all__ = ['Command']
