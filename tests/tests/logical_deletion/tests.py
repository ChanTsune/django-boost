from datetime import timedelta

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
        item.delete()
        self.assertNotEqual(item.deleted_at, None)

    def test_delete_with_deleted_at(self):
        self._register_items(*[str(i) for i in range(10)])
        deleted_at = now() - timedelta(days=1)
        item = self.model.objects.get(name="0")
        item.delete(deleted_at=deleted_at)
        item.refresh_from_db()
        self.assertEqual(item.deleted_at, deleted_at)

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
        self.model.objects.delete()
        self.assertEqual(len(self.model.objects.dead()), 10)
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
