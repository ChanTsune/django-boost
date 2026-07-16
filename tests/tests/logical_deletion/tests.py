from datetime import date, datetime, timedelta, timezone as datetime_timezone
from unittest import mock
from zoneinfo import ZoneInfo

import django
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models.deletion import ProtectedError
from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.template import Context, Template
from django.test import TestCase, override_settings
from django.test.utils import isolate_apps
from django.utils import timezone
from django.utils.timezone import now

from django_boost.models.deletion import get_logical_delete_field
from django_boost.models.manager import LogicalDeletionManager
from django_boost.models.mixins import LogicalDeletionMixin


@override_settings(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
)
class TestLogicalDeletionMixin(TestCase):
    from .models import LogicalDeletionModel

    model = LogicalDeletionModel

    def _register_items(self, *args):
        for item in args:
            self.model.objects.create(name=item)

    def test_delete(self):
        self._register_items(*[str(i) for i in range(10)])
        item = self.model.objects.get(name="0")
        deleted = item.delete()
        self.assertNotEqual(item.deleted_at, None)
        self.assertEqual(deleted[0], 1)
        self.assertEqual(deleted[1], {self.model._meta.label: 1})

    def test_delete_with_deleted_at(self):
        self._register_items(*[str(i) for i in range(10)])
        deleted_at = now() - timedelta(days=1)
        item = self.model.objects.get(name="0")
        item.delete(deleted_at=deleted_at)
        item.refresh_from_db()
        self.assertEqual(item.deleted_at, deleted_at)

    def test_delete_unsaved_item_raises_value_error(self):
        item = self.model(name="0")
        with self.assertRaises(ValueError):
            item.delete()
        self.assertIsNone(item.pk)
        self.assertEqual(self.model.objects.count(), 0)

    def test_hard_delete(self):
        self._register_items(*[str(i) for i in range(10)])
        item = self.model.objects.get(name="0")
        item.delete(hard=True)
        with self.assertRaises(self.model.DoesNotExist):
            self.model.objects.get(name="0")

    def test_alive(self):
        self._register_items(*[str(i) for i in range(10)])
        item = self.model.objects.get(name="0")
        item.delete()
        self.assertEqual(len(self.model.objects.alive()), 9)

    def test_dead(self):
        self._register_items(*[str(i) for i in range(10)])
        item = self.model.objects.get(name="0")
        item.delete()
        self.assertEqual(len(self.model.objects.dead()), 1)

    def test_revive(self):
        self._register_items(*[str(i) for i in range(10)])
        item = self.model.objects.get(name="0")
        item.delete()
        self.assertEqual(len(self.model.objects.dead()), 1)
        self.assertEqual(len(self.model.objects.alive()), 9)
        item.revive()
        self.assertEqual(len(self.model.objects.dead()), 0)
        self.assertEqual(len(self.model.objects.alive()), 10)

    def test_revive_forwards_save_arguments(self):
        from unittest import mock

        self._register_items("0")
        item = self.model.objects.get(name="0")
        item.delete()
        with mock.patch.object(item, "save") as save:
            item.revive(force_update=True, using="other")
        save.assert_called_once_with(force_update=True, using="other")
        self.assertIsNone(item.deleted_at)

    def test_is_dead(self):
        self._register_items(*[str(i) for i in range(10)])
        item = self.model.objects.get(name="0")
        item.delete()
        self.assertTrue(item.is_dead())

    def test_is_alive(self):
        self._register_items(*[str(i) for i in range(10)])
        item = self.model.objects.get(name="0")
        self.assertTrue(item.is_alive())


class TestLogicalDeletionManager(TestCase):
    from .models import LogicalDeletionModel

    model = LogicalDeletionModel

    def _register_items(self, *args):
        for item in args:
            self.model.objects.create(name=item)

    def _hard_delete(self):
        for i in self.model.objects.all():
            i.delete(hard=True)

    def test_delete(self):
        self._register_items(*[str(i) for i in range(10)])
        deleted = self.model.objects.delete()
        self.assertEqual(len(self.model.objects.dead()), 10)
        self.assertEqual(deleted[0], 10)
        self.assertEqual(deleted[1], {self.model._meta.label: 10})
        self._hard_delete()

    def test_delete_with_deleted_at(self):
        self._register_items(*[str(i) for i in range(10)])
        deleted_at = now() - timedelta(days=1)
        self.model.objects.delete(deleted_at=deleted_at)
        for item in self.model.objects.dead():
            self.assertEqual(item.deleted_at, deleted_at)
        self._hard_delete()

    def test_queryset_delete_with_deleted_at(self):
        self._register_items(*[str(i) for i in range(10)])
        deleted_at = now() - timedelta(days=1)
        self.model.objects.filter(name__in=["0", "1"]).delete(deleted_at=deleted_at)
        self.assertEqual(len(self.model.objects.dead()), 2)
        for item in self.model.objects.dead():
            self.assertEqual(item.deleted_at, deleted_at)
        self._hard_delete()

    def test_distinct_fields_queryset_delete_raises_type_error(self):
        # .distinct(*fields) is rejected on every supported Django version.
        self._register_items(*[str(i) for i in range(10)])
        with self.assertRaises(TypeError):
            self.model.objects.distinct("name").delete()
        self.assertEqual(len(self.model.objects.alive()), 10)
        self._hard_delete()

    def test_plain_distinct_queryset_delete_matches_django_version(self):
        # Django <5.0 rejects a plain .distinct().delete(); 5.0+ allows it.
        self._register_items(*[str(i) for i in range(10)])
        if django.VERSION >= (5, 0):
            self.model.objects.distinct().delete()
            self.assertEqual(len(self.model.objects.dead()), 10)
        else:
            with self.assertRaises(TypeError):
                self.model.objects.distinct().delete()
            self.assertEqual(len(self.model.objects.alive()), 10)
        self._hard_delete()

    def test_values_queryset_delete_raises_type_error(self):
        self._register_items(*[str(i) for i in range(10)])
        with self.assertRaises(TypeError):
            self.model.objects.values("id").delete()
        self.assertEqual(len(self.model.objects.alive()), 10)
        self._hard_delete()

    def test_sliced_queryset_delete_raises_type_error(self):
        # Django rejects delete() on a sliced queryset; logical delete matches.
        self._register_items(*[str(i) for i in range(10)])
        with self.assertRaises(TypeError):
            self.model.objects.all()[:2].delete()
        self.assertEqual(len(self.model.objects.alive()), 10)
        self._hard_delete()

    def test_hard_delete(self):
        self._register_items(*[str(i) for i in range(10)])
        self.model.objects.delete(hard=True)
        self.assertEqual(len(self.model.objects.dead()), 0)
        self.assertEqual(len(self.model.objects.alive()), 0)
        self.assertEqual(len(self.model.objects.all()), 0)
        self._hard_delete()

    def test_revive(self):
        self._register_items(*[str(i) for i in range(10)])
        self.model.objects.delete()
        self.assertEqual(len(self.model.objects.dead()), 10)
        self.assertEqual(len(self.model.objects.alive()), 0)
        self.assertEqual(len(self.model.objects.all()), 10)

        self.model.objects.revive()
        self.assertEqual(len(self.model.objects.dead()), 0)
        self.assertEqual(len(self.model.objects.alive()), 10)
        self.assertEqual(len(self.model.objects.all()), 10)
        self._hard_delete()


class TestLogicalDeletionDateLookups(TestCase):
    """deleted_since/deleted_before/deleted_between on the queryset and manager."""

    from .models import LogicalDeletionModel

    model = LogicalDeletionModel
    # A past date on purpose: if the timezone.now mock ever stopped
    # applying, a frozen "today" would keep passing until the next day.
    now = datetime(2026, 1, 15, 12, tzinfo=datetime_timezone.utc)

    def setUp(self):
        self.alive = self.model.objects.create(name='alive')
        self.deleted = {
            days: self.model.objects.create(
                name=str(days), deleted_at=self.now - timedelta(days=days))
            for days in (0, 6, 7, 8, 9)
        }

    def _ids(self, queryset):
        return set(queryset.values_list('pk', flat=True))

    def test_deleted_since_is_inclusive_of_today_and_the_boundary_day(self):
        # deleted_since(9) covers today plus the 8 preceding days (offset 8
        # inclusive); offset 9 falls outside that span.
        with mock.patch('django_boost.models.query.timezone.now', return_value=self.now):
            manager_ids = self._ids(self.model.objects.deleted_since(9))
            queryset_ids = self._ids(
                self.model.objects.filter(pk__gt=0).deleted_since(9))

        expected = {self.deleted[days].pk for days in (0, 6, 7, 8)}
        self.assertEqual(manager_ids, expected)
        self.assertEqual(queryset_ids, expected)
        self.assertNotIn(self.deleted[9].pk, manager_ids)
        self.assertNotIn(self.alive.pk, manager_ids)

    def test_deleted_before_excludes_the_boundary_day_itself(self):
        boundary = self.now.date() - timedelta(days=7)
        with mock.patch('django_boost.models.query.timezone.now', return_value=self.now):
            manager_ids = self._ids(self.model.objects.deleted_before(boundary))
            queryset_ids = self._ids(
                self.model.objects.filter(pk__gt=0).deleted_before(boundary))

        expected = {self.deleted[days].pk for days in (8, 9)}
        self.assertEqual(manager_ids, expected)
        self.assertEqual(queryset_ids, expected)
        self.assertNotIn(self.deleted[7].pk, manager_ids)
        self.assertNotIn(self.alive.pk, manager_ids)

    def test_deleted_between_is_inclusive_of_both_boundary_days(self):
        start = self.now.date() - timedelta(days=8)
        end = self.now.date() - timedelta(days=7)
        with mock.patch('django_boost.models.query.timezone.now', return_value=self.now):
            manager_ids = self._ids(
                self.model.objects.deleted_between(start=start, end=end))
            queryset_ids = self._ids(
                self.model.objects.filter(pk__gt=0).deleted_between(
                    start=start, end=end))

        expected = {self.deleted[days].pk for days in (7, 8)}
        self.assertEqual(manager_ids, expected)
        self.assertEqual(queryset_ids, expected)
        self.assertNotIn(self.deleted[6].pk, manager_ids)  # day after end
        self.assertNotIn(self.deleted[9].pk, manager_ids)  # day before start
        self.assertNotIn(self.alive.pk, manager_ids)

    def test_deleted_between_start_only_leaves_the_upper_bound_open(self):
        start = self.now.date() - timedelta(days=8)
        with mock.patch('django_boost.models.query.timezone.now', return_value=self.now):
            ids = self._ids(self.model.objects.deleted_between(start=start))

        self.assertEqual(ids, {self.deleted[days].pk for days in (0, 6, 7, 8)})
        self.assertNotIn(self.deleted[9].pk, ids)
        self.assertNotIn(self.alive.pk, ids)

    def test_deleted_between_end_only_leaves_the_lower_bound_open(self):
        end = self.now.date() - timedelta(days=7)
        with mock.patch('django_boost.models.query.timezone.now', return_value=self.now):
            ids = self._ids(self.model.objects.deleted_between(end=end))

        self.assertEqual(ids, {self.deleted[days].pk for days in (7, 8, 9)})
        self.assertNotIn(self.deleted[6].pk, ids)
        self.assertNotIn(self.alive.pk, ids)

    def test_deleted_since_excludes_a_future_dated_deletion(self):
        # A deleted_at on a future calendar day (e.g. a scheduled delete) must
        # not count as within the past N days. A later time on the current day
        # would still count: the window runs to the start of tomorrow.
        future = self.model.objects.create(
            name='future', deleted_at=self.now + timedelta(days=5))
        with mock.patch('django_boost.models.query.timezone.now', return_value=self.now):
            ids = self._ids(self.model.objects.deleted_since(1))

        self.assertNotIn(future.pk, ids)

    def test_deleted_since_zero_days_matches_nothing(self):
        with mock.patch('django_boost.models.query.timezone.now', return_value=self.now):
            self.assertFalse(self.model.objects.deleted_since(0).exists())

    def test_deleted_between_with_no_bounds_returns_all_deleted_items(self):
        manager_ids = self._ids(self.model.objects.deleted_between())
        queryset_ids = self._ids(
            self.model.objects.filter(pk__gt=0).deleted_between())

        expected = {item.pk for item in self.deleted.values()}
        self.assertEqual(manager_ids, expected)
        self.assertEqual(queryset_ids, expected)
        self.assertNotIn(self.alive.pk, manager_ids)

    def test_deleted_before_localizes_an_aware_datetime_boundary(self):
        # 20:00 UTC on Jan 8 is already Jan 9 in Asia/Tokyo, so the cutoff must
        # be the start of Jan 9 JST; the row deleted at Jan 8 12:00 UTC stays
        # included.
        boundary = datetime(2026, 1, 8, 20, tzinfo=datetime_timezone.utc)
        with timezone.override(ZoneInfo('Asia/Tokyo')):
            ids = self._ids(self.model.objects.deleted_before(boundary))

        self.assertEqual(ids, {self.deleted[days].pk for days in (7, 8, 9)})


class TestLogicalDeletionDjangoDeleteCompatibility(TestCase):
    from .models import (LogicalDeletionChild, LogicalDeletionNullableChild,
                         LogicalDeletionParent, LogicalDeletionProtectedChild,
                         LogicalDeletionSetChild, NonFastPhysicalChild,
                         NonFastPhysicalGrandChild, PhysicalCascadeChild)

    parent_model = LogicalDeletionParent
    child_model = LogicalDeletionChild
    nullable_child_model = LogicalDeletionNullableChild
    set_child_model = LogicalDeletionSetChild
    protected_child_model = LogicalDeletionProtectedChild
    physical_child_model = PhysicalCascadeChild
    nonfast_child_model = NonFastPhysicalChild
    nonfast_grandchild_model = NonFastPhysicalGrandChild

    def test_instance_delete_sends_delete_signals_without_save_signals(self):
        parent = self.parent_model.objects.create(name="parent")
        events = []

        def receiver(name):
            def _receiver(sender, instance, **kwargs):
                if sender is self.parent_model:
                    events.append(name)
            return _receiver

        receivers = [
            (pre_delete, receiver("pre_delete")),
            (post_delete, receiver("post_delete")),
            (pre_save, receiver("pre_save")),
            (post_save, receiver("post_save")),
        ]
        for signal, handler in receivers:
            signal.connect(handler, weak=False)
        try:
            parent.delete()
        finally:
            for signal, handler in receivers:
                signal.disconnect(handler)

        self.assertEqual(events, ["pre_delete", "post_delete"])

    def test_instance_delete_cascades_to_logical_children(self):
        deleted_at = now() - timedelta(days=1)
        parent = self.parent_model.objects.create(name="parent")
        child = self.child_model.objects.create(parent=parent, name="child")

        deleted = parent.delete(deleted_at=deleted_at)

        parent.refresh_from_db()
        child.refresh_from_db()
        self.assertEqual(parent.deleted_at, deleted_at)
        self.assertEqual(child.deleted_at, deleted_at)
        self.assertEqual(deleted[0], 2)
        self.assertEqual(deleted[1], {
            self.parent_model._meta.label: 1,
            self.child_model._meta.label: 1,
        })

    def test_queryset_delete_cascades_to_logical_children(self):
        deleted_at = now() - timedelta(days=1)
        parent = self.parent_model.objects.create(name="parent")
        child = self.child_model.objects.create(parent=parent, name="child")

        deleted = self.parent_model.objects.filter(pk=parent.pk).delete(
            deleted_at=deleted_at)

        parent.refresh_from_db()
        child.refresh_from_db()
        self.assertEqual(parent.deleted_at, deleted_at)
        self.assertEqual(child.deleted_at, deleted_at)
        self.assertEqual(deleted[0], 2)
        self.assertEqual(deleted[1], {
            self.parent_model._meta.label: 1,
            self.child_model._meta.label: 1,
        })

    def test_instance_delete_honors_protected_related_objects(self):
        parent = self.parent_model.objects.create(name="parent")
        self.protected_child_model.objects.create(parent=parent, name="child")

        with self.assertRaises(ProtectedError):
            parent.delete()

        parent.refresh_from_db()
        self.assertIsNone(parent.deleted_at)

    def test_queryset_delete_honors_protected_related_objects(self):
        parent = self.parent_model.objects.create(name="parent")
        self.protected_child_model.objects.create(parent=parent, name="child")

        with self.assertRaises(ProtectedError):
            self.parent_model.objects.filter(pk=parent.pk).delete()

        parent.refresh_from_db()
        self.assertIsNone(parent.deleted_at)

    def test_instance_delete_applies_set_null_related_updates(self):
        parent = self.parent_model.objects.create(name="parent")
        child = self.nullable_child_model.objects.create(
            parent=parent, name="child")

        parent.delete()

        child.refresh_from_db()
        self.assertIsNone(child.parent_id)
        self.assertIsNone(child.deleted_at)

    def test_instance_delete_physically_cascades_non_logical_children(self):
        parent = self.parent_model.objects.create(name="parent")
        child = self.physical_child_model.objects.create(
            parent=parent, name="child")

        deleted = parent.delete()

        parent.refresh_from_db()
        self.assertTrue(parent.is_dead())
        self.assertFalse(self.physical_child_model.objects.filter(
            pk=child.pk).exists())
        self.assertEqual(deleted[0], 2)
        self.assertEqual(deleted[1], {
            self.parent_model._meta.label: 1,
            self.physical_child_model._meta.label: 1,
        })

    def test_instance_delete_physically_cascades_non_fast_deletable_child(self):
        # The grandchild makes the non-logical child non-fast-deletable, so it is
        # physically deleted through Collector.data rather than fast_deletes,
        # while the logical parent is soft-deleted. Matches Django physical delete.
        parent = self.parent_model.objects.create(name="parent")
        child = self.nonfast_child_model.objects.create(parent=parent, name="c")
        grandchild = self.nonfast_grandchild_model.objects.create(
            parent=child, name="gc")

        deleted = parent.delete()

        parent.refresh_from_db()
        self.assertTrue(parent.is_dead())
        self.assertFalse(
            self.nonfast_child_model.objects.filter(pk=child.pk).exists())
        self.assertFalse(
            self.nonfast_grandchild_model.objects.filter(pk=grandchild.pk).exists())
        self.assertEqual(deleted[0], 3)
        self.assertEqual(deleted[1], {
            self.parent_model._meta.label: 1,
            self.nonfast_child_model._meta.label: 1,
            self.nonfast_grandchild_model._meta.label: 1,
        })

    def test_instance_delete_applies_set_callable_related_updates(self):
        # on_delete=SET(callable) is non-lazy: Django evaluates the related
        # queryset during collect() and applies the value to the materialized
        # instances. The child's FK is set, and the child itself is not deleted.
        parent = self.parent_model.objects.create(name="parent")
        child = self.set_child_model.objects.create(parent=parent, name="child")

        parent.delete()

        child.refresh_from_db()
        self.assertIsNone(child.parent_id)
        self.assertIsNone(child.deleted_at)


class GetLogicalDeleteFieldTests(TestCase):

    def test_resolves_field_via_manager_attribute_fallback(self):
        # A logical model whose default manager exposes only the delete_flag_field
        # attribute (no get_deleted_flag_field_name method) still resolves its
        # delete-flag field, so the collector soft-deletes instead of hard-deleting.
        with isolate_apps("tests"):
            class AttrManager(models.Manager):
                delete_flag_field = "deleted_at"

            class PlainManagerModel(LogicalDeletionMixin):
                objects = AttrManager()

                class Meta:
                    app_label = "tests"

            field = get_logical_delete_field(PlainManagerModel)

        self.assertIsNotNone(field)
        self.assertEqual(field.name, "deleted_at")

    def test_raises_when_delete_flag_field_does_not_exist(self):
        # A misconfigured delete flag field fails loud instead of silently
        # degrading to a physical delete.
        with isolate_apps("tests"):
            class MissingFieldManager(models.Manager):
                delete_flag_field = "missing_field"

            class MisconfiguredModel(LogicalDeletionMixin):
                objects = MissingFieldManager()

                class Meta:
                    app_label = "tests"

            with self.assertRaises(ImproperlyConfigured):
                get_logical_delete_field(MisconfiguredModel)


class LogicalDeletionManagerCustomFieldTests(TestCase):
    """A custom delete_flag_field on the manager must reach its queryset, so
    alive()/dead()/revive() filter on the right column."""

    def test_custom_delete_flag_field_propagates_to_queryset(self):
        with isolate_apps("tests"):
            class RemovedManager(LogicalDeletionManager):
                delete_flag_field = "removed_at"

            class CustomFieldModel(models.Model):
                removed_at = models.DateTimeField(null=True, default=None)
                objects = RemovedManager()

                class Meta:
                    app_label = "tests"

            queryset = CustomFieldModel.objects.get_queryset()

        self.assertEqual(queryset.get_delete_flag_field_name(), "removed_at")

    def test_custom_delete_flag_field_survives_clone(self):
        with isolate_apps("tests"):
            class RemovedManager(LogicalDeletionManager):
                delete_flag_field = "removed_at"

            class CustomFieldModel(models.Model):
                removed_at = models.DateTimeField(null=True, default=None)
                objects = RemovedManager()

                class Meta:
                    app_label = "tests"

            # A cloning method (filter/all/order_by) must not drop the custom
            # field; alive() on the clone must filter on removed_at, not the
            # class-default deleted_at (which would raise FieldError).
            queryset = CustomFieldModel.objects.filter(pk__gt=0).alive()

        self.assertEqual(queryset.get_delete_flag_field_name(), "removed_at")

    def test_custom_delete_flag_field_reaches_date_lookups(self):
        with isolate_apps("tests"):
            class RemovedManager(LogicalDeletionManager):
                delete_flag_field = "removed_at"

            class CustomFieldModel(models.Model):
                removed_at = models.DateTimeField(null=True, default=None)
                objects = RemovedManager()

                class Meta:
                    app_label = "tests"

            today = date(2026, 7, 16)
            querysets = (
                CustomFieldModel.objects.deleted_since(7),
                CustomFieldModel.objects.deleted_before(today),
                CustomFieldModel.objects.deleted_between(start=today, end=today),
            )

        # The generated SQL must reference removed_at, not the class-default
        # deleted_at.
        for queryset in querysets:
            self.assertIn("removed_at", str(queryset.query))


class AltersDataTests(TestCase):
    """Data-altering logical-deletion methods must not be callable from
    templates, matching Django's own Model.delete/QuerySet.delete/update."""
    from .models import LogicalDeletionModel

    model = LogicalDeletionModel

    def test_instance_revive_is_not_called_by_templates(self):
        item = self.model.objects.create(name="0")
        item.delete()

        Template("{{ object.revive }}").render(Context({"object": item}))

        item.refresh_from_db()
        self.assertIsNotNone(item.deleted_at)

    def test_queryset_revive_is_not_called_by_templates(self):
        item = self.model.objects.create(name="1")
        item.delete()
        queryset = self.model.objects.filter(pk=item.pk)

        Template("{{ queryset.revive }}").render(Context({"queryset": queryset}))

        item.refresh_from_db()
        self.assertIsNotNone(item.deleted_at)

    def test_manager_delete_is_not_called_by_templates(self):
        item = self.model.objects.create(name="2")

        Template("{{ manager.delete }}").render(
            Context({"manager": self.model.objects}))

        item.refresh_from_db()
        self.assertIsNone(item.deleted_at)

    def test_manager_revive_is_not_called_by_templates(self):
        item = self.model.objects.create(name="3")
        item.delete()

        Template("{{ manager.revive }}").render(
            Context({"manager": self.model.objects}))

        item.refresh_from_db()
        self.assertIsNotNone(item.deleted_at)


class ManagerOnlyLogicalDeletionTests(TestCase):
    """LogicalDeletionManager must still soft-delete when the model does not
    inherit LogicalDeletionMixin (manager-only configuration)."""
    from .models import ManagerOnlyLogicalDeletionModel

    model = ManagerOnlyLogicalDeletionModel

    def test_delete_marks_row_dead_instead_of_removing_it(self):
        item = self.model.objects.create(name="0")

        self.model.objects.filter(pk=item.pk).delete()

        item.refresh_from_db()
        self.assertIsNotNone(item.deleted_at)
        self.assertEqual(self.model.objects.count(), 1)

    def test_alive_and_dead_reflect_the_delete(self):
        item = self.model.objects.create(name="0")

        self.model.objects.filter(pk=item.pk).delete()

        self.assertEqual(self.model.objects.alive().count(), 0)
        self.assertEqual(self.model.objects.dead().count(), 1)
