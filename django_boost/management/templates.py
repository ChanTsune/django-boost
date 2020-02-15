from os import path

from django.core.management.templates import TemplateCommand as DjangoTemplateCommand

import django_boost
from django_boost.core.management import CommandVersion


class TemplateCommand(CommandVersion, DjangoTemplateCommand):

    def handle_template(self, template, subdir):
        if template is None:
            return path.join(django_boost.__path__[0], 'conf', subdir)
        return super().handle_template(template, subdir)
