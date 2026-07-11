"""Admin list filters for Django's ``django.contrib.admin``."""

from __future__ import annotations

from datetime import datetime, time, timedelta

from django.contrib import admin
from django.contrib.admin.filters import ListFilter
from django.core.exceptions import ValidationError
from django.forms import DateField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


__all__ = ["LogicalDeletedDateFilter", "LogicalDeletedFilter"]


class LogicalDeletedFilter(admin.SimpleListFilter):
    """Admin list filter for alive/dead items on a ``LogicalDeletionMixin`` model."""

    title = 'delete state'
    parameter_name = 'delete_state'

    def lookups(self, request, model_admin):  # noqa: D102
        return (
            ('alive', ('Alive')),
            ('dead', ('Dead')),
        )

    def queryset(self, request, queryset):  # noqa: D102
        value = self.value()
        if value == 'alive':
            return queryset.alive()
        if value == 'dead':
            return queryset.dead()

    def choices(self, changelist):  # noqa: D102
        for index, choice in enumerate(super().choices(changelist)):
            if index == 1:
                choice = dict(choice)
                choice['query_string'] = changelist.get_query_string(
                    {self.parameter_name: 'alive'},
                    [
                        LogicalDeletedDateFilter.period_parameter,
                        LogicalDeletedDateFilter.from_parameter,
                        LogicalDeletedDateFilter.to_parameter,
                    ],
                )
            yield choice


class LogicalDeletedDateFilter(admin.FieldListFilter):
    """Filter logically deleted objects by common periods or an inclusive date range."""

    template = 'boost/admin/logical_deleted_date_filter.html'
    title = _('deleted date')

    period_parameter = 'deleted_period'
    from_parameter = 'deleted_from'
    to_parameter = 'deleted_to'

    def __init__(self, field, request, params, model, model_admin, field_path):  # noqa: D107
        self.field = field
        self.field_path = field_path
        self.lookup_choices = (
            ('all_deleted', _('All deleted')),
            ('today', _('Today')),
            ('past_7_days', _('Past 7 days')),
            ('past_30_days', _('Past 30 days')),
            ('past_90_days', _('Past 90 days')),
            ('older_than_90_days', _('More than 90 days ago')),
        )
        ListFilter.__init__(self, request, params, model, model_admin)
        for parameter in self.expected_parameters():
            if parameter in params:
                value = params.pop(parameter)
                if isinstance(value, (list, tuple)):
                    value = value[-1]
                self.used_parameters[parameter] = value

        excluded = set(self.expected_parameters()) | {'delete_state', 'p'}
        self.preserved_parameters = [
            (key, value)
            for key, values in request.GET.lists()
            if key not in excluded
            for value in values
        ]
        self.errors = []

    def expected_parameters(self):  # noqa: D102
        return [self.period_parameter, self.from_parameter, self.to_parameter]

    def has_output(self):  # noqa: D102
        return True

    def choices(self, changelist):  # noqa: D102
        own_parameters = self.expected_parameters()
        has_range = bool(self.from_value or self.to_value)
        yield {
            'selected': self.value() is None and not has_range,
            'query_string': changelist.get_query_string(remove=own_parameters),
            'display': _('All'),
        }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup and not has_range,
                'query_string': changelist.get_query_string(
                    {self.period_parameter: lookup},
                    [self.from_parameter, self.to_parameter, 'delete_state'],
                ),
                'display': title,
            }

    def value(self):
        """Return the selected preset period."""
        return self.used_parameters.get(self.period_parameter)

    @property
    def from_value(self):
        """Return the submitted inclusive start date."""
        return self.used_parameters.get(self.from_parameter, '')

    @property
    def to_value(self):
        """Return the submitted inclusive end date."""
        return self.used_parameters.get(self.to_parameter, '')

    def queryset(self, request, queryset):  # noqa: D102
        if self.from_value or self.to_value:
            return self._range_queryset(queryset)

        today = self._local_today()
        tomorrow = self._start_of_day(today + timedelta(days=1))
        period = self.value()
        lookups = {}
        if period == 'all_deleted':
            lookups[f'{self.field_path}__isnull'] = False
        elif period == 'today':
            lookups[f'{self.field_path}__gte'] = self._start_of_day(today)
            lookups[f'{self.field_path}__lt'] = tomorrow
        elif period in {'past_7_days', 'past_30_days', 'past_90_days'}:
            days = int(period.split('_')[1])
            lookups[f'{self.field_path}__gte'] = self._start_of_day(
                today - timedelta(days=days - 1))
            lookups[f'{self.field_path}__lt'] = tomorrow
        elif period == 'older_than_90_days':
            lookups[f'{self.field_path}__lt'] = self._start_of_day(
                today - timedelta(days=89))
        else:
            return queryset
        return queryset.filter(**lookups)

    def _range_queryset(self, queryset):
        date_field = DateField(input_formats=['%Y-%m-%d'])
        start = end = None
        try:
            if self.from_value:
                start = date_field.clean(self.from_value)
            if self.to_value:
                end = date_field.clean(self.to_value)
        except ValidationError as error:
            self.errors.extend(error.messages)
            return queryset

        if start and end and start > end:
            self.errors.append(_('Start date must be on or before end date.'))
            return queryset

        lookups = {}
        if start:
            lookups[f'{self.field_path}__gte'] = self._start_of_day(start)
        if end:
            lookups[f'{self.field_path}__lt'] = self._start_of_day(
                end + timedelta(days=1))
        return queryset.filter(**lookups)

    @staticmethod
    def _local_today():
        now = timezone.now()
        if timezone.is_aware(now):
            now = timezone.localtime(now)
        return now.date()

    @staticmethod
    def _start_of_day(value):
        result = datetime.combine(value, time.min)
        if timezone.is_aware(timezone.now()):
            result = timezone.make_aware(result, timezone.get_current_timezone())
        return result
