from __future__ import annotations

import os
import shutil
import tempfile
from os import path

from django.core.management.templates import TemplateCommand as DjangoTemplateCommand

import django_boost
from django_boost.core.management import CommandVersion


class TemplateCommand(CommandVersion, DjangoTemplateCommand):

    def handle_template(self, template, subdir):
        base = super().handle_template(template, subdir)
        # Only enhance the built-in template; a user-supplied --template is left untouched.
        if template is not None:
            return base
        overlay = path.join(django_boost.__path__[0], 'conf', subdir)
        if not path.isdir(overlay):
            return base
        return self._compose(base, overlay)

    def _compose(self, base, overlay):
        """Layer django-boost's extra files onto Django's base template.

        Files already shipped by ``base`` win, so anything Django starts
        providing under the same name supersedes our overlay automatically.
        """
        composed = tempfile.mkdtemp()
        self.paths_to_remove.append(composed)
        shutil.copytree(base, composed, dirs_exist_ok=True)
        for root, _dirs, files in os.walk(overlay):
            rel = path.relpath(root, overlay)
            dst_dir = composed if rel == os.curdir else path.join(composed, rel)
            for name in files:
                dst = path.join(dst_dir, name)
                if path.exists(dst):
                    continue
                os.makedirs(dst_dir, exist_ok=True)
                shutil.copy2(path.join(root, name), dst)
        return composed
