from django import template

register = template.Library()


@register.filter
def filter(queryset, arg):
    k, v = arg.split("=")
    return queryset.filter(**{k: v})


@register.filter
def order_by(queryset, arg):
    return queryset.order_by(arg)


@register.filter
def exclude(queryset, arg):
    k, v = arg.split("=")
    return queryset.exclude(**{k: v})


@register.filter
def dead(queryset):
    if hasattr(queryset, 'dead') and callable(queryset.dead):
        return queryset.dead()
    return queryset


@register.filter
def alive(qureyset):
    if hasattr(qureyset, 'alive') and callable(qureyset, 'alive'):
        return qureyset.alive()
    return qureyset
