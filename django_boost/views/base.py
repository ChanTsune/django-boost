"""Static-file views built on Django's native generic views."""

from __future__ import annotations

import mimetypes
import os

from django.core.exceptions import ImproperlyConfigured
from django.http import FileResponse, Http404
from django.views import View as _View


__all__ = ["StaticView"]


class StaticResponseMixin:
    static_name = None
    content_type = None

    def get_static_names(self):
        if self.static_name is None:
            raise ImproperlyConfigured(
                "StaticResponseMixin requires either a definition of "
                "'static_name' or an implementation of 'get_static_names()'")
        return [self.static_name]

    def create_response(self):
        names = self.get_static_names()
        for path in names:
            if os.path.exists(path):
                encoding = None
                if self.content_type is None:
                    content_type, encoding = mimetypes.guess_type(path)
                    content_type = content_type or 'application/octet-stream'
                else:
                    content_type = self.content_type
                response = FileResponse(
                    open(path, 'rb'), content_type=content_type)
                if encoding:
                    response["Content-Encoding"] = encoding
                return response
        raise FileNotFoundError('%s does not exist.' % ', '.join(names))


class StaticView(StaticResponseMixin, _View):
    """View that serves a single static file, e.g. via ``include_static_files``."""

    def get(self, request, *args, **kwargs):  # noqa: D102
        try:
            return self.create_response()
        except FileNotFoundError:
            # A file present when the route was registered may be gone at
            # request time; serve 404 as Django's own static view does.
            raise Http404
