"""Admin list filters for Django's ``django.contrib.admin``."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any, Iterator, TYPE_CHECKING, cast

from django.contrib import admin
from django.contrib.admin.filters import ListFilter
from django.contrib.admin.views.main import ChangeList
from django.core.exceptions import ValidationError
from django.db.models import Model, QuerySet
from django.forms import DateField
from django.http import HttpRequest
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django_boost.models.query import LogicalDeletionQuerySet

if TYPE_CHECKING:
    from django.contrib.admin.filters import _ListFilterChoices

__all__ = ["LogicalDeletedDateFilter", "LogicalDeletedFilter"]


class LogicalDeletedFilter(admin.SimpleListFilter):
    """Admin list filter for alive/dead items on a ``LogicalDeletionMixin`` model."""

    title = 'delete state'
    parameter_name = 'delete_state'

    def lookups(  # noqa: D102
        self, request: HttpRequest, model_admin: admin.ModelAdmin,
    ) -> tuple[tuple[str, str], tuple[str, str]]:
        return (
            ('alive', ('Alive')),
            ('dead', ('Dead')),
        )

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet | None:  # noqa: D102
        value = self.value()
        # SimpleListFilter's declared queryset type is the base QuerySet, but
        # this filter only ever attaches to LogicalDeletionMixin models, whose
        # managers return LogicalDeletionQuerySet (alive()/dead()).
        qs = cast(LogicalDeletionQuerySet, queryset)
        if value == 'alive':
            return cast(QuerySet, qs.alive())
        if value == 'dead':
            return cast(QuerySet, qs.dead())
        return None

    def choices(self, changelist: ChangeList) -> Iterator[_ListFilterChoices]:  # noqa: D102
        for index, choice in enumerate(super().choices(changelist)):
            if index == 1:
                choice = cast("_ListFilterChoices", dict(choice))
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

    # This filter only ever stores plain strings (see __init__), unlike the
    # base ListFilter.used_parameters: dict[str, object] -- same narrowing
    # django-stubs itself applies for SimpleListFilter.
    used_parameters: dict[str, str]  # type: ignore[assignment]

    template = 'boost/admin/logical_deleted_date_filter.html'
    title = _('deleted date')

    period_parameter = 'deleted_period'
    from_parameter = 'deleted_from'
    to_parameter = 'deleted_to'

    def __init__(  # noqa: D107
        self,
        field: Any,
        request: HttpRequest,
        # django-stubs types ListFilter.__init__'s params as dict[str, str] on
        # 5.1.3 (CI's Django 4.2 cell) but dict[str, list[str]] on 6.0.6 (CI's
        # Django 5.2 cell); dict[str, Any] satisfies both.
        params: dict[str, Any],
        model: type[Model],
        model_admin: admin.ModelAdmin,
        field_path: str,
    ) -> None:
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
                raw = params.pop(parameter)
                self.used_parameters[parameter] = raw[-1] if isinstance(raw, (list, tuple)) else raw

        excluded = set(self.expected_parameters()) | {'delete_state', 'p'}
        self.preserved_parameters = [
            (key, value)
            for key, values in request.GET.lists()
            if key not in excluded
            for value in values
        ]
        self.errors: list[Any] = []

    def expected_parameters(self) -> list[str | None]:  # noqa: D102
        return [self.period_parameter, self.from_parameter, self.to_parameter]

    def has_output(self) -> bool:  # noqa: D102
        return True

    def choices(self, changelist: ChangeList) -> Iterator[_ListFilterChoices]:  # noqa: D102
        # expected_parameters()'s return type is widened to match the base
        # ListFilter signature, but this override never actually includes None.
        own_parameters = cast("list[str]", self.expected_parameters())
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

    def value(self) -> str | None:
        """Return the selected preset period."""
        return self.used_parameters.get(self.period_parameter)

    @property
    def from_value(self) -> str:
        """Return the submitted inclusive start date."""
        return self.used_parameters.get(self.from_parameter, '')

    @property
    def to_value(self) -> str:
        """Return the submitted inclusive end date."""
        return self.used_parameters.get(self.to_parameter, '')

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet:  # noqa: D102
        # LogicalDeletedDateFilter only ever attaches to LogicalDeletionMixin
        # models, same as LogicalDeletedFilter above.
        qs = cast(LogicalDeletionQuerySet, queryset)
        if self.from_value or self.to_value:
            return self._range_queryset(qs)

        period = self.value()
        if period == 'all_deleted':
            return cast(QuerySet, qs.dead())
        if period == 'today':
            return cast(QuerySet, qs.deleted_since(1))
        if period in {'past_7_days', 'past_30_days', 'past_90_days'}:
            days = int(period.split('_')[1])
            return cast(QuerySet, qs.deleted_since(days))
        if period == 'older_than_90_days':
            return cast(QuerySet, qs.deleted_before(self._local_today() - timedelta(days=89)))
        return cast(QuerySet, qs)

    def _range_queryset(self, queryset: LogicalDeletionQuerySet) -> QuerySet:
        date_field = DateField(input_formats=['%Y-%m-%d'])
        start: date | None = None
        end: date | None = None
        try:
            if self.from_value:
                start = date_field.clean(self.from_value)
            if self.to_value:
                end = date_field.clean(self.to_value)
        except ValidationError as error:
            self.errors.extend(error.messages)
            return cast(QuerySet, queryset)

        if start and end and start > end:
            self.errors.append(_('Start date must be on or before end date.'))
            return cast(QuerySet, queryset)

        return cast(QuerySet, queryset.deleted_between(start=start, end=end))

    @staticmethod
    def _local_today() -> date:
        now = timezone.now()
        if timezone.is_aware(now):
            now = timezone.localtime(now)
        return now.date()
