"""This module provides queryset methods for django template."""

from __future__ import annotations

from django import template

register = template.Library()


@register.filter
def filter(queryset, arg):
    """Filter ``queryset`` by a single ``"field=value"`` argument."""
    k, v = arg.split("=", 1)
    return queryset.filter(**{k: v})


@register.filter
def order_by(queryset, arg):  # noqa: D103
    return queryset.order_by(arg)


@register.filter
def exclude(queryset, arg):
    """Exclude from ``queryset`` by a single ``"field=value"`` argument."""
    k, v = arg.split("=", 1)
    return queryset.exclude(**{k: v})


@register.filter
def dead(queryset):
    """Return the queryset's dead items via its ``dead`` manager method, if available, else unchanged."""
    if hasattr(queryset, 'dead') and callable(queryset.dead):
        return queryset.dead()
    return queryset


@register.filter
def alive(queryset):
    """Return the queryset's alive items via its ``alive`` manager method, if available, else unchanged."""
    if hasattr(queryset, 'alive') and callable(queryset.alive):
        return queryset.alive()
    return queryset
