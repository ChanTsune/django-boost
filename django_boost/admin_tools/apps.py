from django.apps import AppConfig


class AdminToolsConfig(AppConfig):
    name = 'django_boost.admin_tools'

    def ready(self):
        # Implement your startup processing
        pass
