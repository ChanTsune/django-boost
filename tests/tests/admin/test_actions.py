from django.contrib.admin import AdminSite, ModelAdmin
from django.test import RequestFactory, TestCase

from django_boost.admin.actions import hard_delete_selected
from django_boost.admin.mixins import LogicalDeletionModelAdminMixin
from tests.models import RelatedItemModel


class _AllowAllUser:
    is_active = True
    is_superuser = True
    pk = 1

    def has_perm(self, perm, obj=None):
        return True


class _SpyAdmin(LogicalDeletionModelAdminMixin, ModelAdmin):
    """Records which logging API the action used, without touching LogEntry."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logged_bulk = False
        self.logged_single = 0

    def get_deleted_objects(self, queryset, request):
        return ([], {}, [], [])

    def hard_delete_queryset(self, request, queryset):
        pass

    def message_user(self, *args, **kwargs):
        pass

    def log_deletions(self, request, queryset):
        self.logged_bulk = True

    def log_deletion(self, request, obj, obj_display):
        self.logged_single += 1


class _FallbackAdmin:
    """A model admin without log_deletions (as on Django 4.2/5.0), providing
    only what the confirmed hard-delete path touches."""

    def __init__(self, model):
        self.model = model
        self.opts = model._meta
        self.logged_single = 0

    def get_deleted_objects(self, queryset, request):
        return ([], {}, [], [])

    def hard_delete_queryset(self, request, queryset):
        pass

    def message_user(self, *args, **kwargs):
        pass

    def log_deletion(self, request, obj, obj_display):
        self.logged_single += 1


class HardDeleteLoggingTests(TestCase):
    """The confirmed hard-delete must use the bulk log_deletions() API rather
    than the per-object log_deletion() deprecated in Django 5.1."""

    def _confirmed_request(self):
        request = RequestFactory().post("/", {"post": "yes"})
        request.user = _AllowAllUser()
        return request

    def test_confirmed_hard_delete_uses_bulk_logging(self):
        admin = _SpyAdmin(RelatedItemModel, AdminSite())
        RelatedItemModel.objects.create(name="a")

        hard_delete_selected(
            admin, self._confirmed_request(), RelatedItemModel.objects.all())

        self.assertTrue(admin.logged_bulk)
        self.assertEqual(admin.logged_single, 0)

    def test_confirmed_hard_delete_falls_back_to_per_object_logging(self):
        admin = _FallbackAdmin(RelatedItemModel)
        RelatedItemModel.objects.create(name="a")

        hard_delete_selected(
            admin, self._confirmed_request(), RelatedItemModel.objects.all())

        self.assertEqual(admin.logged_single, 1)
