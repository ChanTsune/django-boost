from datetime import datetime, timedelta, timezone as datetime_timezone
from unittest import mock
from zoneinfo import ZoneInfo

from django.contrib.admin import AdminSite, ModelAdmin
from django.template.loader import render_to_string
from django.test import RequestFactory, TestCase
from django.utils import timezone

from django_boost.admin.filters import LogicalDeletedDateFilter, LogicalDeletedFilter
from django_boost.admin.mixins import LogicalDeletionModelAdminMixin
from tests.tests.logical_deletion.models import LogicalDeletionModel


class _AllowAllUser:
    is_active = True
    is_staff = True
    is_superuser = True

    def has_perm(self, perm, obj=None):
        return True


class _LogicalDeletionAdmin(LogicalDeletionModelAdminMixin, ModelAdmin):
    pass


class LogicalDeletedDateFilterTests(TestCase):
    """Tests for deletion-date presets and inclusive custom ranges."""

    model = LogicalDeletionModel
    now = datetime(2026, 7, 11, 12, tzinfo=datetime_timezone.utc)

    def setUp(self):
        self.factory = RequestFactory()
        self.model_admin = ModelAdmin(self.model, AdminSite())
        self.alive = self.model.objects.create(name='alive')
        self.deleted = {
            days: self.model.objects.create(
                name=str(days), deleted_at=self.now - timedelta(days=days))
            for days in (0, 6, 7, 29, 89, 90)
        }

    def _filter(self, **parameters):
        request = self.factory.get('/', parameters)
        params = {key: request.GET.getlist(key) for key in request.GET}
        field = self.model._meta.get_field('deleted_at')
        return LogicalDeletedDateFilter(
            field, request, params, self.model, self.model_admin,
            field_path='deleted_at')

    def _filtered_ids(self, **parameters):
        filter_ = self._filter(**parameters)
        with mock.patch('django_boost.admin.filters.timezone.now', return_value=self.now):
            queryset = filter_.queryset(None, self.model.objects.all())
        return set(queryset.values_list('pk', flat=True))

    def _changelist(self, **parameters):
        request = self.factory.get('/', parameters)
        request.user = _AllowAllUser()
        model_admin = _LogicalDeletionAdmin(self.model, AdminSite())
        return model_admin.get_changelist_instance(request)

    @staticmethod
    def _date_filter(changelist):
        return next(
            filter_
            for filter_ in changelist.filter_specs
            if isinstance(filter_, LogicalDeletedDateFilter)
        )

    def test_all_deleted_excludes_alive_objects(self):
        self.assertEqual(
            self._filtered_ids(deleted_period='all_deleted'),
            {item.pk for item in self.deleted.values()},
        )

    def test_today_uses_the_current_local_calendar_day(self):
        self.assertEqual(
            self._filtered_ids(deleted_period='today'),
            {self.deleted[0].pk},
        )

    def test_past_periods_cover_the_named_number_of_calendar_days(self):
        self.assertEqual(
            self._filtered_ids(deleted_period='past_7_days'),
            {self.deleted[0].pk, self.deleted[6].pk},
        )
        self.assertEqual(
            self._filtered_ids(deleted_period='past_30_days'),
            {self.deleted[days].pk for days in (0, 6, 7, 29)},
        )
        self.assertEqual(
            self._filtered_ids(deleted_period='past_90_days'),
            {self.deleted[days].pk for days in (0, 6, 7, 29, 89)},
        )

    def test_older_than_90_days_does_not_overlap_past_90_days(self):
        self.assertEqual(
            self._filtered_ids(deleted_period='older_than_90_days'),
            {self.deleted[90].pk},
        )

    def test_custom_range_includes_both_submitted_dates(self):
        self.assertEqual(
            self._filtered_ids(deleted_from='2026-07-04', deleted_to='2026-07-05'),
            {self.deleted[6].pk, self.deleted[7].pk},
        )

    def test_custom_range_accepts_a_single_boundary(self):
        self.assertEqual(
            self._filtered_ids(deleted_to='2026-04-12'),
            {self.deleted[90].pk},
        )

    def test_custom_range_accepts_start_only(self):
        self.assertEqual(
            self._filtered_ids(deleted_from='2026-07-04'),
            {self.deleted[days].pk for days in (0, 6, 7)},
        )

    def test_custom_range_same_day_includes_the_whole_day(self):
        at_start = self.model.objects.create(
            name='start',
            deleted_at=datetime(2026, 7, 5, tzinfo=datetime_timezone.utc),
        )
        at_end = self.model.objects.create(
            name='end',
            deleted_at=datetime(
                2026, 7, 5, 23, 59, 59, tzinfo=datetime_timezone.utc),
        )
        next_day = self.model.objects.create(
            name='next',
            deleted_at=datetime(2026, 7, 6, tzinfo=datetime_timezone.utc),
        )

        filtered_ids = self._filtered_ids(
            deleted_from='2026-07-05', deleted_to='2026-07-05')

        self.assertEqual(
            filtered_ids,
            {self.deleted[6].pk, at_start.pk, at_end.pk},
        )
        self.assertNotIn(next_day.pk, filtered_ids)

    def test_no_period_returns_the_unfiltered_queryset(self):
        expected = set(self.model.objects.values_list('pk', flat=True))

        self.assertEqual(self._filtered_ids(), expected)
        self.assertEqual(
            self._filtered_ids(deleted_period='unknown-period'), expected)

    def test_django_42_scalar_parameters_are_not_truncated(self):
        request = self.factory.get('/', {'deleted_from': '2026-07-04'})
        field = self.model._meta.get_field('deleted_at')

        filter_ = LogicalDeletedDateFilter(
            field,
            request,
            {'deleted_from': '2026-07-04'},
            self.model,
            self.model_admin,
            field_path='deleted_at',
        )

        self.assertEqual(filter_.from_value, '2026-07-04')

    def test_invalid_range_is_ignored_and_exposes_an_error(self):
        filter_ = self._filter(
            deleted_from='2026-07-12', deleted_to='2026-07-11')

        queryset = filter_.queryset(None, self.model.objects.all())

        self.assertEqual(set(queryset), set(self.model.objects.all()))
        self.assertEqual(
            filter_.errors,
            ['Start date must be on or before end date.'],
        )

    def test_invalid_date_is_ignored_and_exposes_an_error(self):
        filter_ = self._filter(deleted_from='not-a-date')

        queryset = filter_.queryset(None, self.model.objects.all())

        self.assertEqual(set(queryset), set(self.model.objects.all()))
        self.assertTrue(filter_.errors)

    def test_model_admin_changelist_accepts_range_parameters(self):
        request = self.factory.get(
            '/', {'deleted_from': '2026-07-04', 'deleted_to': '2026-07-05'})
        request.user = _AllowAllUser()
        model_admin = _LogicalDeletionAdmin(self.model, AdminSite())

        changelist = model_admin.get_changelist_instance(request)

        self.assertEqual(
            set(changelist.result_list.values_list('pk', flat=True)),
            {self.deleted[6].pk, self.deleted[7].pk},
        )

    def test_state_filter_returns_alive_and_dead_objects(self):
        alive = self._changelist(delete_state='alive')
        dead = self._changelist(delete_state='dead')

        self.assertEqual(
            set(alive.result_list.values_list('pk', flat=True)),
            {self.alive.pk},
        )
        self.assertEqual(
            set(dead.result_list.values_list('pk', flat=True)),
            {item.pk for item in self.deleted.values()},
        )

    def test_date_filter_choices_select_the_current_preset(self):
        changelist = self._changelist(
            deleted_period='past_30_days', delete_state='alive', q='article')
        choices = list(self._date_filter(changelist).choices(changelist))

        selected = [choice for choice in choices if choice['selected']]

        self.assertEqual(len(selected), 1)
        self.assertEqual(str(selected[0]['display']), 'Past 30 days')
        self.assertIn('deleted_period=past_30_days', selected[0]['query_string'])
        self.assertIn('q=article', selected[0]['query_string'])
        self.assertNotIn('delete_state', selected[0]['query_string'])
        self.assertNotIn('deleted_from', selected[0]['query_string'])
        self.assertNotIn('deleted_to', selected[0]['query_string'])

    def test_custom_range_marks_no_preset_as_selected(self):
        changelist = self._changelist(
            deleted_from='2026-07-04', deleted_to='2026-07-05', q='article')
        choices = list(self._date_filter(changelist).choices(changelist))

        self.assertFalse(any(choice['selected'] for choice in choices))
        self.assertIn('q=article', choices[0]['query_string'])
        self.assertNotIn('deleted_from', choices[0]['query_string'])
        self.assertNotIn('deleted_to', choices[0]['query_string'])

    def test_range_form_preserves_only_unrelated_changelist_parameters(self):
        filter_ = self._filter(
            deleted_period='past_30_days',
            deleted_from='2026-07-04',
            deleted_to='2026-07-05',
            delete_state='alive',
            p='2',
            q='article',
            o='1',
            category=['news', 'release'],
        )

        self.assertEqual(
            filter_.preserved_parameters,
            [
                ('q', 'article'),
                ('o', '1'),
                ('category', 'news'),
                ('category', 'release'),
            ],
        )

    def test_alive_choice_clears_an_active_deletion_date_range(self):
        request = self.factory.get(
            '/', {'deleted_from': '2026-07-04', 'deleted_to': '2026-07-05'})
        request.user = _AllowAllUser()
        model_admin = _LogicalDeletionAdmin(self.model, AdminSite())
        changelist = model_admin.get_changelist_instance(request)
        state_filter = next(
            filter_
            for filter_ in changelist.filter_specs
            if isinstance(filter_, LogicalDeletedFilter)
        )

        alive_choice = list(state_filter.choices(changelist))[1]

        self.assertIn('delete_state=alive', alive_choice['query_string'])
        self.assertNotIn('deleted_from', alive_choice['query_string'])
        self.assertNotIn('deleted_to', alive_choice['query_string'])

    def test_range_form_template_renders_submitted_values_and_errors(self):
        filter_ = self._filter(
            deleted_from='2026-07-12', deleted_to='2026-07-11')
        filter_.queryset(None, self.model.objects.all())

        html = render_to_string(
            filter_.template,
            {
                'title': filter_.title,
                'choices': [
                    {
                        'selected': False,
                        'query_string': '?',
                        'display': 'All',
                    },
                ],
                'spec': filter_,
            },
        )

        self.assertIn('type="date"', html)
        self.assertIn('value="2026-07-12"', html)
        self.assertIn('Start date must be on or before end date.', html)

    def test_today_uses_the_current_non_utc_timezone(self):
        local_today = self.model.objects.create(
            name='local',
            deleted_at=datetime(2026, 7, 11, 15, tzinfo=datetime_timezone.utc),
        )
        previous_local_day = self.model.objects.create(
            name='prior',
            deleted_at=datetime(
                2026, 7, 11, 14, 59, 59, tzinfo=datetime_timezone.utc),
        )
        now = datetime(2026, 7, 11, 15, 30, tzinfo=datetime_timezone.utc)

        with timezone.override(ZoneInfo('Asia/Tokyo')):
            with mock.patch(
                    'django_boost.admin.filters.timezone.now', return_value=now):
                queryset = self._filter(
                    deleted_period='today').queryset(
                        None, self.model.objects.all())

        filtered_ids = set(queryset.values_list('pk', flat=True))
        self.assertEqual(filtered_ids, {local_today.pk})
        self.assertNotIn(previous_local_day.pk, filtered_ids)

    def test_custom_range_uses_the_current_non_utc_timezone(self):
        at_start = self.model.objects.create(
            name='tzstart',
            deleted_at=datetime(2026, 7, 11, 15, tzinfo=datetime_timezone.utc),
        )
        before_start = self.model.objects.create(
            name='tzprior',
            deleted_at=datetime(
                2026, 7, 11, 14, 59, 59, tzinfo=datetime_timezone.utc),
        )
        at_end = self.model.objects.create(
            name='tzend',
            deleted_at=datetime(
                2026, 7, 12, 14, 59, 59, tzinfo=datetime_timezone.utc),
        )
        next_day = self.model.objects.create(
            name='tznext',
            deleted_at=datetime(2026, 7, 12, 15, tzinfo=datetime_timezone.utc),
        )

        with timezone.override(ZoneInfo('Asia/Tokyo')):
            queryset = self._filter(
                deleted_from='2026-07-12', deleted_to='2026-07-12',
            ).queryset(None, self.model.objects.all())

        filtered_ids = set(queryset.values_list('pk', flat=True))
        self.assertEqual(filtered_ids, {at_start.pk, at_end.pk})
        self.assertNotIn(before_start.pk, filtered_ids)
        self.assertNotIn(next_day.pk, filtered_ids)
