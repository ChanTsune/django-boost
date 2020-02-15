from django.conf import settings
from django.core.checks import Warning


def check_database_router(app_configs, **kwargs):
    db_router = "django_boost.db.router.DatabaseRouter"
    errors = []
    if hasattr(settings, "DATABASE_ROUTERS"):
        if db_router in settings.DATABASE_ROUTERS:
            if not hasattr(settings, "DATABASE_APPS_MAPPING"):
                errors.append(
                    Warning("Use '%s', but 'DATABASE_APPS_MAPPING'"
                            " is not set in settings" % db_router,
                            hint="Set app_label to key and "
                            "database name to value for dict",
                            obj=db_router)
                )
    return errors
