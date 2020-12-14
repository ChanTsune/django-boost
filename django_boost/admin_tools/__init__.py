import django

if django.VERSION < (3, 2):
    default_app_config = "django_boost.admin_tools.apps.AdminToolsConfig"
