"""The ``startapp_plus`` management command."""

from __future__ import annotations

from django_boost.management.templates import TemplateCommand


class Command(TemplateCommand):  # noqa: D101
    help = (
        "Creates a Django app directory structure for the given app name in "
        "the current directory or optionally in the given directory."
    )
    missing_args_message = "You must provide an application name."

    def handle(self, *args, **options):  # noqa: D102
        app_name = options.pop('name')
        target = options.pop('directory')
        template_type = 'app'
        return super().handle(template_type, app_name, target, **options)
