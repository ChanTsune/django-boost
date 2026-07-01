from django.contrib.admin import AdminSite, ModelAdmin
from django.contrib.auth.models import Group, User
from django.test import RequestFactory, SimpleTestCase

from django_boost.admin.mixins import LogicalDeletionModelAdminMixin


class _AllowAllUser:
    is_active = True
    is_superuser = True

    def has_perm(self, perm, obj=None):
        return True


class LogicalAdmin(LogicalDeletionModelAdminMixin, ModelAdmin):
    pass


class LogicalDeletionAdminActionLeakTests(SimpleTestCase):
    """The hard-delete action must stay on the logical-deletion admin, not
    leak onto unrelated model admins sharing the same AdminSite."""

    def setUp(self):
        self.factory = RequestFactory()

    def _request(self):
        request = self.factory.get("/")
        request.user = _AllowAllUser()
        return request

    def test_hard_delete_action_does_not_leak_to_other_model_admins(self):
        site = AdminSite()
        logical_admin = LogicalAdmin(User, site)
        plain_admin = ModelAdmin(Group, site)

        # Baseline: an unrelated admin has no hard-delete action.
        self.assertNotIn("hard_delete_selected", plain_admin.get_actions(self._request()))

        # Rendering the logical-deletion admin's actions must not change that.
        logical_admin.get_actions(self._request())

        self.assertNotIn("hard_delete_selected", plain_admin.get_actions(self._request()))

    def test_hard_delete_action_is_available_on_the_logical_deletion_admin(self):
        site = AdminSite()
        logical_admin = LogicalAdmin(User, site)

        self.assertIn("hard_delete_selected", logical_admin.get_actions(self._request()))
