from unittest import mock

from django.test import TestCase, TransactionTestCase, override_settings

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


class RoutingHintSpyRouter:
    """Records the hints each db_for_write call receives, without deciding
    anything itself (returns None so the default router still applies)."""

    calls = []

    def db_for_write(self, model, **hints):
        type(self).calls.append(hints)
        return None


@override_settings(DATABASE_ROUTERS=[
    'tests.tests.models.fields.test_related_descriptors.RoutingHintSpyRouter'])
class AutoReverseOneToOneRoutingTests(TestCase):
    """AutoReverseOneToOneDescriptor's creation path must hint db_for_write
    with the parent instance, the same way Django's own reverse-descriptor
    read path already does, so a hint-based router (e.g. sharding by
    instance) can route the created row to the parent's database."""

    def setUp(self):
        RoutingHintSpyRouter.calls = []

    def test_creation_hints_db_for_write_with_the_parent_instance(self):
        parent = AutoOneToOneParentModel.objects.create(name='p')
        RoutingHintSpyRouter.calls = []

        parent.child

        # The existence check get_or_create() performs before creating is the
        # first db_for_write call; it must carry the instance hint so a
        # hint-based router sees the same context Django's own read path
        # already gets, instead of an unhinted lookup.
        first_write_hints = RoutingHintSpyRouter.calls[0]
        self.assertEqual(first_write_hints.get('instance'), parent)


@override_settings(
    DATABASE_APPS_MAPPING={'tests': 'example'},
    # Re-set DATABASE_ROUTERS (even to its existing value) so the
    # setting_changed signal forces DatabaseRouter to reload the mapping
    # above; it snapshots DATABASE_APPS_MAPPING in __init__ otherwise.
    DATABASE_ROUTERS=['django_boost.db.router.DatabaseRouter'])
class AutoReverseOneToOneAtomicAliasTests(TransactionTestCase):
    """The transaction guarding creation must target the alias the router
    resolves for the parent, not be hardcoded to 'default'."""

    databases = {'default', 'example'}

    def setUp(self):
        # The 'tests' app has no migrations of its own and was never synced
        # onto 'example' at test-database setup time (it wasn't mapped there
        # yet); sync it now so the rerouted writes below have a table to hit.
        # TransactionTestCase (not TestCase): sqlite's schema editor cannot
        # run inside the wrapping atomic() a plain TestCase would use here.
        from django.core.management import call_command
        call_command('migrate', run_syncdb=True, database='example',
                     verbosity=0)

    def test_atomic_targets_the_resolved_alias_not_default(self):
        import django_boost.models.fields.related_descriptors as related_descriptors

        used_aliases = []
        real_atomic = related_descriptors.atomic

        def spy_atomic(*args, **kwargs):
            using = kwargs.get('using', args[0] if args else None)
            used_aliases.append(using)
            return real_atomic(*args, **kwargs)

        parent = AutoOneToOneParentModel.objects.create(name='p')
        with mock.patch.object(related_descriptors, 'atomic', spy_atomic):
            parent.child

        self.assertIn('example', used_aliases)
        self.assertNotIn('default', used_aliases)
