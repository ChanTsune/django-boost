from django.test import TestCase

from tests.models import AutoOneToOneChildModel, AutoOneToOneParentModel


class AutoReverseOneToOneDescriptorTests(TestCase):
    """`AutoOneToOneField` auto-creates the related object for a saved parent,
    but an unsaved parent has no pk to create against, so accessing the reverse
    relation must raise the same `RelatedObjectDoesNotExist` a plain
    `OneToOneField` would (not a leaked ORM `ValueError`)."""

    def test_unsaved_parent_raises_related_object_does_not_exist(self):
        parent = AutoOneToOneParentModel(name='unsaved')
        with self.assertRaises(AutoOneToOneChildModel.DoesNotExist):
            parent.child

    def test_saved_parent_auto_creates_child(self):
        parent = AutoOneToOneParentModel.objects.create(name='saved')
        child = parent.child
        self.assertIsInstance(child, AutoOneToOneChildModel)
        self.assertEqual(child.parent_id, parent.pk)
