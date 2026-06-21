from datetime import timedelta

from django.db.models.deletion import ProtectedError
from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.test import TestCase, override_settings
from django.utils.timezone import now


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

    def test_distinct_queryset_delete_raises_type_error(self):
        self._register_items(*[str(i) for i in range(10)])
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


class TestLogicalDeletionDjangoDeleteCompatibility(TestCase):
    from .models import (LogicalDeletionChild, LogicalDeletionNullableChild,
                         LogicalDeletionParent, LogicalDeletionProtectedChild,
                         PhysicalCascadeChild)

    parent_model = LogicalDeletionParent
    child_model = LogicalDeletionChild
    nullable_child_model = LogicalDeletionNullableChild
    protected_child_model = LogicalDeletionProtectedChild
    physical_child_model = PhysicalCascadeChild

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
