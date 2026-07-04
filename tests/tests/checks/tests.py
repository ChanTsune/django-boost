from types import SimpleNamespace
from unittest.mock import patch

from django.apps import apps
from django.db import models
from django.test import override_settings
from django.test.utils import isolate_apps

from django_boost.checks import (
    DATABASE_ROUTER,
    EMAILUSER_MODEL,
    REDIRECT_CORRECT_HOSTNAME_MIDDLEWARE,
    USER_AGENT_CONTEXT_PROCESSOR,
    _app_labels,
    _check_logical_deletion_model,
    _correct_host_has_invalid_format,
    _correct_host_is_allowed,
    check_admin_tools_requires_admin,
    check_database_router,
    check_emailuser_deprecated,
    check_logical_deletion_models,
    check_redirect_correct_hostname_middleware,
    check_user_agent_extra,
)
from django_boost.db.router import DatabaseRouter
from django_boost.models.mixins import LogicalDeletionMixin
from django_boost.test import TestCase

from tests.models import RelatedItemModel
from tests.tests.logical_deletion.models import LogicalDeletionModel


def check_ids(messages):
    return [message.id for message in messages]


class DatabaseRouterCheckTests(TestCase):

    @override_settings(DATABASE_ROUTERS=(), DATABASE_APPS_MAPPING={"missing": "missing"})
    def test_no_warning_when_router_is_absent(self):
        self.assertEqual(check_database_router(None), [])

    def test_missing_mapping(self):
        fake_settings = SimpleNamespace(
            DATABASE_ROUTERS=[DATABASE_ROUTER],
            DATABASES={"default": {}},
        )
        with patch("django_boost.checks.settings", fake_settings):
            messages = check_database_router(None)

        self.assertEqual(check_ids(messages), ["django_boost.W001"])

    def test_router_string_setting_is_detected(self):
        fake_settings = SimpleNamespace(
            DATABASE_ROUTERS=DATABASE_ROUTER,
            DATABASES={"default": {}},
        )
        with patch("django_boost.checks.settings", fake_settings):
            messages = check_database_router(None)

        self.assertEqual(check_ids(messages), ["django_boost.W001"])

    def test_router_instance_is_detected(self):
        fake_settings = SimpleNamespace(
            DATABASE_ROUTERS=[DatabaseRouter()],
            DATABASES={"default": {}},
        )
        with patch("django_boost.checks.settings", fake_settings):
            messages = check_database_router(None)

        self.assertEqual(check_ids(messages), ["django_boost.W001"])

    def test_router_class_is_detected(self):
        fake_settings = SimpleNamespace(
            DATABASE_ROUTERS=[DatabaseRouter],
            DATABASES={"default": {}},
        )
        with patch("django_boost.checks.settings", fake_settings):
            messages = check_database_router(None)

        self.assertEqual(check_ids(messages), ["django_boost.W001"])

    def test_app_labels_is_none_until_app_registry_is_ready(self):
        with patch("django_boost.checks.apps", SimpleNamespace(ready=False)):
            self.assertIsNone(_app_labels())

    @override_settings(DATABASE_ROUTERS=[DATABASE_ROUTER], DATABASE_APPS_MAPPING=["tests"])
    def test_invalid_mapping_type(self):
        messages = check_database_router(None)

        self.assertEqual(check_ids(messages), ["django_boost.E001"])

    @override_settings(
        DATABASE_ROUTERS=[DATABASE_ROUTER],
        DATABASE_APPS_MAPPING={"tests": "missing"},
    )
    def test_unknown_database_alias(self):
        messages = check_database_router(None)

        self.assertEqual(check_ids(messages), ["django_boost.E002"])

    @override_settings(
        DATABASE_ROUTERS=[DATABASE_ROUTER],
        DATABASE_APPS_MAPPING={"missing_app": "default"},
    )
    def test_unknown_app_label(self):
        messages = check_database_router(None)

        self.assertEqual(check_ids(messages), ["django_boost.W002"])

    @override_settings(DATABASE_ROUTERS=[DATABASE_ROUTER], DATABASE_APPS_MAPPING={})
    def test_empty_mapping_is_valid(self):
        self.assertEqual(check_database_router(None), [])

    @override_settings(
        DATABASE_ROUTERS=[DATABASE_ROUTER],
        DATABASE_APPS_MAPPING={"tests": "default"},
    )
    def test_known_app_label_is_valid_when_app_configs_are_limited(self):
        app_configs = [apps.get_app_config("auth")]

        self.assertEqual(check_database_router(app_configs), [])


class RedirectCorrectHostnameMiddlewareCheckTests(TestCase):

    @override_settings(MIDDLEWARE=(), DEBUG=False)
    def test_no_warning_when_middleware_is_absent(self):
        self.assertEqual(check_redirect_correct_hostname_middleware(None), [])

    @override_settings(
        MIDDLEWARE=[REDIRECT_CORRECT_HOSTNAME_MIDDLEWARE],
        DEBUG=False,
        CORRECT_HOST=None,
        ALLOWED_HOSTS=["example.com"],
    )
    def test_missing_correct_host_in_production(self):
        messages = check_redirect_correct_hostname_middleware(None)

        self.assertEqual(check_ids(messages), ["django_boost.W010"])

    @override_settings(
        MIDDLEWARE=REDIRECT_CORRECT_HOSTNAME_MIDDLEWARE,
        DEBUG=False,
        CORRECT_HOST=None,
        ALLOWED_HOSTS=["example.com"],
    )
    def test_middleware_string_setting_is_detected(self):
        messages = check_redirect_correct_hostname_middleware(None)

        self.assertEqual(check_ids(messages), ["django_boost.W010"])

    @override_settings(
        MIDDLEWARE=[REDIRECT_CORRECT_HOSTNAME_MIDDLEWARE],
        DEBUG=True,
        CORRECT_HOST="https://example.com",
    )
    def test_invalid_correct_host_format(self):
        messages = check_redirect_correct_hostname_middleware(None)

        self.assertEqual(check_ids(messages), ["django_boost.W011"])

    @override_settings(
        MIDDLEWARE=[REDIRECT_CORRECT_HOSTNAME_MIDDLEWARE],
        DEBUG=False,
        CORRECT_HOST="canonical.example.com",
        ALLOWED_HOSTS=["example.com"],
    )
    def test_correct_host_not_allowed(self):
        messages = check_redirect_correct_hostname_middleware(None)

        self.assertEqual(check_ids(messages), ["django_boost.W012"])

    @override_settings(
        MIDDLEWARE=[REDIRECT_CORRECT_HOSTNAME_MIDDLEWARE],
        DEBUG=False,
        CORRECT_HOST="example.com:8000",
        ALLOWED_HOSTS=["example.com"],
    )
    def test_correct_host_with_port_matches_allowed_host(self):
        self.assertEqual(check_redirect_correct_hostname_middleware(None), [])

    @override_settings(
        MIDDLEWARE=[REDIRECT_CORRECT_HOSTNAME_MIDDLEWARE],
        DEBUG=False,
        CORRECT_HOST="canonical.example.com",
        ALLOWED_HOSTS=["*"],
    )
    def test_wildcard_allowed_hosts_is_valid(self):
        self.assertEqual(check_redirect_correct_hostname_middleware(None), [])

    def test_non_string_correct_host_is_not_allowed(self):
        self.assertFalse(_correct_host_is_allowed(object(), ["example.com"]))

    def test_non_string_correct_host_has_invalid_format(self):
        self.assertTrue(_correct_host_has_invalid_format(object()))


class UserAgentExtraCheckTests(TestCase):

    @override_settings(TEMPLATES=[{"OPTIONS": {"context_processors": []}}])
    def test_no_error_when_context_processor_is_absent(self):
        with patch("django_boost.checks.find_spec", return_value=None):
            self.assertEqual(check_user_agent_extra(None), [])

    @override_settings(
        TEMPLATES=[{"OPTIONS": {"context_processors": [USER_AGENT_CONTEXT_PROCESSOR]}}],
    )
    def test_error_when_context_processor_is_configured_and_extra_is_missing(self):
        with patch("django_boost.checks.find_spec", return_value=None):
            messages = check_user_agent_extra(None)

        self.assertEqual(check_ids(messages), ["django_boost.E020"])

    @override_settings(
        TEMPLATES=[{"OPTIONS": {"context_processors": [USER_AGENT_CONTEXT_PROCESSOR]}}],
    )
    def test_no_error_when_context_processor_is_configured_and_extra_is_importable(self):
        with patch("django_boost.checks.find_spec", return_value=object()):
            self.assertEqual(check_user_agent_extra(None), [])

    @override_settings(
        TEMPLATES=[{"OPTIONS": {"context_processors": [USER_AGENT_CONTEXT_PROCESSOR]}}],
    )
    def test_error_when_dependency_lookup_fails(self):
        with patch("django_boost.checks.find_spec", side_effect=ModuleNotFoundError):
            messages = check_user_agent_extra(None)

        self.assertEqual(check_ids(messages), ["django_boost.E020"])


class LogicalDeletionCheckTests(TestCase):

    def test_no_warning_for_normal_model(self):
        self.assertEqual(_check_logical_deletion_model(RelatedItemModel), [])

    def test_no_warning_for_correctly_configured_logical_deletion_model(self):
        self.assertEqual(_check_logical_deletion_model(LogicalDeletionModel), [])

    def test_model_check_uses_app_registry(self):
        messages = check_logical_deletion_models(None)

        self.assertNotIn("django_boost.W030", check_ids(messages))
        self.assertNotIn("django_boost.W031", check_ids(messages))

    def test_model_check_supports_limited_app_configs(self):
        app_configs = [apps.get_app_config("auth")]

        self.assertEqual(check_logical_deletion_models(app_configs), [])

    def test_broken_default_manager(self):
        with isolate_apps("tests"):
            class BrokenManagerModel(LogicalDeletionMixin):
                name = models.CharField(max_length=8)
                objects = models.Manager()

                class Meta:
                    app_label = "tests"

            messages = _check_logical_deletion_model(BrokenManagerModel)

        self.assertEqual(check_ids(messages), ["django_boost.W031"])

    def test_non_nullable_deleted_at(self):
        with isolate_apps("tests"):
            class NonNullableDeletedAtModel(LogicalDeletionMixin):
                name = models.CharField(max_length=8)
                deleted_at = models.DateTimeField()

                class Meta:
                    app_label = "tests"

            messages = _check_logical_deletion_model(NonNullableDeletedAtModel)

        self.assertEqual(check_ids(messages), ["django_boost.W032"])

    def test_missing_deleted_at(self):
        with isolate_apps("tests"):
            class MissingDeletedAtModel(LogicalDeletionMixin):
                deleted_at = None
                name = models.CharField(max_length=8)

                class Meta:
                    app_label = "tests"

            messages = _check_logical_deletion_model(MissingDeletedAtModel)

        self.assertEqual(check_ids(messages), ["django_boost.W030"])


class AdminToolsCheckTests(TestCase):

    def test_no_warning_when_admin_is_installed(self):
        self.assertEqual(check_admin_tools_requires_admin(None), [])

    def test_warns_when_contrib_admin_tools_without_django_admin(self):
        with patch(
            "django_boost.checks.apps.is_installed",
            side_effect=lambda name: name == "django_boost.contrib.admin_tools",
        ):
            messages = check_admin_tools_requires_admin(None)
        self.assertEqual(check_ids(messages), ["django_boost.W040"])

    def test_warns_when_legacy_admin_tools_without_django_admin(self):
        with patch(
            "django_boost.checks.apps.is_installed",
            side_effect=lambda name: name == "django_boost.admin_tools",
        ):
            messages = check_admin_tools_requires_admin(None)
        self.assertEqual(check_ids(messages), ["django_boost.W040"])

    def test_no_warning_when_contrib_admin_tools_with_django_admin(self):
        with patch(
            "django_boost.checks.apps.is_installed",
            side_effect=lambda name: name in (
                "django_boost.contrib.admin_tools", "django.contrib.admin"),
        ):
            self.assertEqual(check_admin_tools_requires_admin(None), [])

    def test_no_warning_when_legacy_admin_tools_with_django_admin(self):
        with patch(
            "django_boost.checks.apps.is_installed",
            side_effect=lambda name: name in (
                "django_boost.admin_tools", "django.contrib.admin"),
        ):
            self.assertEqual(check_admin_tools_requires_admin(None), [])

    def test_no_warning_when_admin_tools_absent(self):
        with patch("django_boost.checks.apps.is_installed", return_value=False):
            self.assertEqual(check_admin_tools_requires_admin(None), [])


class EmailUserDeprecationCheckTests(TestCase):

    def test_warns_when_emailuser_is_active(self):
        fake_settings = SimpleNamespace(AUTH_USER_MODEL=EMAILUSER_MODEL)
        with patch("django_boost.checks.settings", fake_settings):
            messages = check_emailuser_deprecated(None)
        self.assertEqual(check_ids(messages), ["django_boost.W050"])

    def test_silent_for_other_user_model(self):
        fake_settings = SimpleNamespace(AUTH_USER_MODEL="auth.User")
        with patch("django_boost.checks.settings", fake_settings):
            self.assertEqual(check_emailuser_deprecated(None), [])
