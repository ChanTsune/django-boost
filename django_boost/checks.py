"""This module provides django_boost application check functions."""

from __future__ import annotations

from importlib.util import find_spec

from django.apps import apps
from django.conf import settings
from django.core.checks import Error, Warning
from django.core.exceptions import FieldDoesNotExist
from django.http.request import split_domain_port, validate_host

DATABASE_ROUTER = "django_boost.db.router.DatabaseRouter"
REDIRECT_CORRECT_HOSTNAME_MIDDLEWARE = "django_boost.middleware.RedirectCorrectHostnameMiddleware"
USER_AGENT_CONTEXT_PROCESSOR = "django_boost.context_processors.user_agent"
USER_AGENTS_PACKAGE = "user_agents"
ADMIN_TOOLS_APP = "django_boost.contrib.admin_tools"
LEGACY_ADMIN_TOOLS_APP = "django_boost.admin_tools"
DJANGO_ADMIN_APP = "django.contrib.admin"
EMAILUSER_MODEL = "django_boost.EmailUser"


def _matches_dotted_path(value, dotted_path):
    if value == dotted_path:
        return True

    module = getattr(value, "__module__", None)
    qualname = getattr(value, "__qualname__", None)
    if module is not None and qualname is not None and "%s.%s" % (module, qualname) == dotted_path:
        return True

    value_class = getattr(value, "__class__", None)
    module = getattr(value_class, "__module__", None)
    qualname = getattr(value_class, "__qualname__", None)
    return module is not None and qualname is not None and "%s.%s" % (module, qualname) == dotted_path


def _setting_contains(setting_name, dotted_path):
    values = getattr(settings, setting_name, ()) or ()
    if isinstance(values, (str, bytes)):
        values = (values,)
    return any(_matches_dotted_path(value, dotted_path) for value in values)


def _app_labels():
    if not apps.ready:
        return None
    return {app_config.label for app_config in apps.get_app_configs()}


def _correct_host_is_allowed(host, allowed_hosts):
    if not isinstance(host, str):
        return False

    domain, _port = split_domain_port(host)
    return bool(domain and validate_host(domain, allowed_hosts or ()))


def _correct_host_has_invalid_format(host):
    if not isinstance(host, str):
        return True
    return host != host.strip() or "://" in host or "/" in host or "\\" in host or any(
        char.isspace() for char in host
    )


def _templates_use_user_agent_context_processor():
    for template_config in getattr(settings, "TEMPLATES", ()):
        context_processors = template_config.get("OPTIONS", {}).get("context_processors", ())
        if USER_AGENT_CONTEXT_PROCESSOR in context_processors:
            return True
    return False


def _user_agents_available():
    try:
        return find_spec(USER_AGENTS_PACKAGE) is not None
    except (ImportError, ValueError):
        return False


def _get_models(app_configs):
    if app_configs is None:
        return apps.get_models()

    models = []
    for app_config in app_configs:
        models.extend(app_config.get_models())
    return models


def check_database_router(app_configs, **kwargs):
    """Validate ``DATABASE_APPS_MAPPING`` when django_boost's router is enabled."""
    errors = []
    if not _setting_contains("DATABASE_ROUTERS", DATABASE_ROUTER):
        return errors

    if not hasattr(settings, "DATABASE_APPS_MAPPING"):
        errors.append(
            Warning(
                "DATABASE_APPS_MAPPING is not set for django-boost's database router.",
                hint="Set DATABASE_APPS_MAPPING to a dict mapping app labels to database aliases.",
                obj=DATABASE_ROUTER,
                id="django_boost.W001",
            )
        )
        return errors

    database_apps_mapping = settings.DATABASE_APPS_MAPPING
    if not isinstance(database_apps_mapping, dict):
        errors.append(
            Error(
                "DATABASE_APPS_MAPPING must be a dict.",
                hint="Set DATABASE_APPS_MAPPING to a dict mapping app labels to database aliases.",
                obj=DATABASE_ROUTER,
                id="django_boost.E001",
            )
        )
        return errors

    database_aliases = set(getattr(settings, "DATABASES", {}))
    app_labels = _app_labels()
    for app_label, database_alias in database_apps_mapping.items():
        if database_alias not in database_aliases:
            errors.append(
                Error(
                    "DATABASE_APPS_MAPPING points '%s' to unknown database alias '%s'."
                    % (app_label, database_alias),
                    hint="Add '%s' to DATABASES or update DATABASE_APPS_MAPPING." % database_alias,
                    obj=DATABASE_ROUTER,
                    id="django_boost.E002",
                )
            )

        if app_labels is not None and app_label not in app_labels:
            errors.append(
                Warning(
                    "DATABASE_APPS_MAPPING contains unknown app label '%s'." % app_label,
                    hint="Use an installed app label in DATABASE_APPS_MAPPING.",
                    obj=DATABASE_ROUTER,
                    id="django_boost.W002",
                )
            )

    return errors


def check_redirect_correct_hostname_middleware(app_configs, **kwargs):
    """Validate ``CORRECT_HOST`` when ``RedirectCorrectHostnameMiddleware`` is enabled."""
    errors = []
    if not _setting_contains("MIDDLEWARE", REDIRECT_CORRECT_HOSTNAME_MIDDLEWARE):
        return errors

    correct_host = getattr(settings, "CORRECT_HOST", None)
    if not correct_host and not settings.DEBUG:
        errors.append(
            Warning(
                "RedirectCorrectHostnameMiddleware is enabled but CORRECT_HOST is not set.",
                hint="Set CORRECT_HOST to the canonical host name or remove the middleware.",
                obj=REDIRECT_CORRECT_HOSTNAME_MIDDLEWARE,
                id="django_boost.W010",
            )
        )
        return errors

    if correct_host and _correct_host_has_invalid_format(correct_host):
        errors.append(
            Warning(
                "CORRECT_HOST has an invalid format.",
                hint='Set CORRECT_HOST to a host name such as "example.com" or "www.example.com".',
                obj=REDIRECT_CORRECT_HOSTNAME_MIDDLEWARE,
                id="django_boost.W011",
            )
        )

    allowed_hosts = getattr(settings, "ALLOWED_HOSTS", ())
    if correct_host and not settings.DEBUG and not _correct_host_is_allowed(correct_host, allowed_hosts):
        errors.append(
            Warning(
                "CORRECT_HOST '%s' is not present in ALLOWED_HOSTS." % correct_host,
                hint="Add CORRECT_HOST to ALLOWED_HOSTS so Django accepts the canonical host.",
                obj=REDIRECT_CORRECT_HOSTNAME_MIDDLEWARE,
                id="django_boost.W012",
            )
        )

    return errors


def check_user_agent_extra(app_configs, **kwargs):
    """Require the optional ``user-agents`` package when the ``user_agent`` context processor is configured."""
    if not _templates_use_user_agent_context_processor() or _user_agents_available():
        return []

    return [
        Error(
            "django_boost.context_processors.user_agent requires the optional user-agents dependency.",
            hint="Install it with `pip install django-boost[useragent]`.",
            obj=USER_AGENT_CONTEXT_PROCESSOR,
            id="django_boost.E020",
        )
    ]


def _check_logical_deletion_model(model):
    from django_boost.models.mixins import LogicalDeletionMixin

    if model is LogicalDeletionMixin or not issubclass(model, LogicalDeletionMixin):
        return []

    errors = []
    try:
        deleted_at = model._meta.get_field("deleted_at")
    except FieldDoesNotExist:
        errors.append(
            Warning(
                "%s.%s uses LogicalDeletionMixin without a deleted_at field."
                % (model._meta.app_label, model.__name__),
                hint="LogicalDeletionMixin expects a nullable deleted_at field.",
                obj=model,
                id="django_boost.W030",
            )
        )
    else:
        if not deleted_at.null:
            errors.append(
                Warning(
                    "%s.%s uses LogicalDeletionMixin with a non-nullable deleted_at field."
                    % (model._meta.app_label, model.__name__),
                    hint="LogicalDeletionMixin expects deleted_at to allow null values.",
                    obj=model,
                    id="django_boost.W032",
                )
            )

    manager = model._default_manager
    missing_methods = [
        method_name for method_name in ("alive", "dead", "revive")
        if not callable(getattr(manager, method_name, None))
    ]
    if missing_methods:
        errors.append(
            Warning(
                "%s.%s uses LogicalDeletionMixin but its default manager lacks logical deletion APIs."
                % (model._meta.app_label, model.__name__),
                hint="Use LogicalDeletionManager or keep the inherited objects manager.",
                obj=model,
                id="django_boost.W031",
            )
        )

    return errors


def check_logical_deletion_models(app_configs, **kwargs):
    """Validate every model using ``LogicalDeletionMixin`` across the project."""
    errors = []
    for model in _get_models(app_configs):
        errors.extend(_check_logical_deletion_model(model))
    return errors


def check_admin_tools_requires_admin(app_configs, **kwargs):
    """Require ``django.contrib.admin`` when an admin_tools app is installed."""
    admin_tools_installed = apps.is_installed(ADMIN_TOOLS_APP) or apps.is_installed(LEGACY_ADMIN_TOOLS_APP)
    if not admin_tools_installed or apps.is_installed(DJANGO_ADMIN_APP):
        return []

    return [
        Warning(
            "django_boost admin_tools is installed without 'django.contrib.admin'.",
            hint="Add 'django.contrib.admin' to INSTALLED_APPS; the adminsitelog command requires it.",
            obj=ADMIN_TOOLS_APP,
            id="django_boost.W040",
        )
    ]


def check_emailuser_deprecated(app_configs, **kwargs):
    """Warn when ``AUTH_USER_MODEL`` still points at the deprecated built-in ``EmailUser``."""
    if getattr(settings, "AUTH_USER_MODEL", None) != EMAILUSER_MODEL:
        return []

    return [
        Warning(
            "AUTH_USER_MODEL uses the deprecated built-in %s." % EMAILUSER_MODEL,
            hint="%s is deprecated and will be removed in django-boost 4.0. Copy the model "
                 "into one of your own apps (keep db_table='django_boost_emailuser') and run "
                 "`manage.py migrate_emailuser`. See the Custom User docs." % EMAILUSER_MODEL,
            obj=EMAILUSER_MODEL,
            id="django_boost.W050",
        )
    ]


CHECKS = (
    check_database_router,
    check_redirect_correct_hostname_middleware,
    check_user_agent_extra,
    check_logical_deletion_models,
    check_admin_tools_requires_admin,
    check_emailuser_deprecated,
)
