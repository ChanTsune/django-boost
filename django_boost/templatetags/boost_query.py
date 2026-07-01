"""This module provides queryset methods for django template."""

from __future__ import annotations

from django import template

register = template.Library()


@register.filter
def filter(queryset, arg):
    k, v = arg.split("=", 1)
    return queryset.filter(**{k: v})


@register.filter
def order_by(queryset, arg):
    return queryset.order_by(arg)


@register.filter
def exclude(queryset, arg):
    k, v = arg.split("=", 1)
    return queryset.exclude(**{k: v})


@register.filter
def dead(queryset):
    if hasattr(queryset, 'dead') and callable(queryset.dead):
        return queryset.dead()
    return queryset


@register.filter
def alive(queryset):
    if hasattr(queryset, 'alive') and callable(queryset.alive):
        return queryset.alive()
    return queryset
