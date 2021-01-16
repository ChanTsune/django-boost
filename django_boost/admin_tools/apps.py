from django.apps import AppConfig


class AdminToolsConfig(AppConfig):
    name = 'admin_tools'

    def ready(self):
        # Implement your startup processing
        pass
