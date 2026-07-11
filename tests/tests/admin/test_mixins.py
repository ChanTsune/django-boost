from django.contrib.admin import AdminSite, ModelAdmin
from django.contrib.auth.models import Group, User
from django.db import models
from django.test import RequestFactory, SimpleTestCase
from django.test.utils import isolate_apps

from django_boost.admin.filters import LogicalDeletedDateFilter, LogicalDeletedFilter
from django_boost.admin.mixins import LogicalDeletionModelAdminMixin
from django_boost.models.manager import LogicalDeletionManager


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

    def test_logical_deletion_filters_are_available(self):
        logical_admin = LogicalAdmin(User, AdminSite())

        self.assertEqual(
            logical_admin.get_list_filter(self._request()),
            [
                LogicalDeletedFilter,
                ('deleted_at', LogicalDeletedDateFilter),
            ],
        )

    def test_date_filter_uses_the_managers_custom_delete_flag_field(self):
        with isolate_apps('tests'):
            class RemovedManager(LogicalDeletionManager):
                delete_flag_field = 'removed_at'

            class CustomFieldModel(models.Model):
                removed_at = models.DateTimeField(null=True, default=None)
                objects = RemovedManager()

                class Meta:
                    app_label = 'tests'

            model_admin = LogicalAdmin(CustomFieldModel, AdminSite())

            self.assertEqual(
                model_admin.get_list_filter(self._request()),
                [
                    LogicalDeletedFilter,
                    ('removed_at', LogicalDeletedDateFilter),
                ],
            )
