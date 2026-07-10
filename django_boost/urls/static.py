"""Extensions for Django's ``django.urls``."""

from __future__ import annotations

import os
import re

from django import urls

from django_boost.views.generic import StaticView


class StaticFileConnector:
    """Builds a list of ``urls.path()`` entries for every file under a directory."""

    def __init__(self, path):
        """Build a ``urls.re_path()`` entry for every file under ``path``."""
        self._urls = []

        for base, _, files in os.walk(path):
            for file in files:
                full_path = os.path.join(base, file)
                url_path = full_path[len(path):]
                if url_path[0] == "/":
                    url_path = url_path[1:]
                # Match the file name literally: re.escape keeps a name like
                # "<x>.js" from being read as a path-converter route.
                self._urls.append(
                    urls.re_path(r"^%s$" % re.escape(url_path),
                                 StaticView.as_view(static_name=full_path)))

    @property
    def urls(self):
        return self._urls


def load_static_files(path):
    """Return the ``urls.path()`` entries built by ``StaticFileConnector`` for every file under ``path``."""
    return StaticFileConnector(path).urls


def include_static_files(path):
    """
    Add to routing that static files under the directory specified by the absolute path.

    example ::

      import os
      from django.urls import path
      from django_boost.urls import include_static_files

      DIR = os.path.dirname(__file__)

      urlpatterns = [
          path('static_files/', include_static_files(DIR)),
      ]
    """
    return urls.include(load_static_files(path))
