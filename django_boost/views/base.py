from __future__ import annotations

import mimetypes
import os
import warnings
from functools import update_wrapper

from django.core.exceptions import ImproperlyConfigured
from django.http import FileResponse, Http404
from django.utils.decorators import classonlymethod
from django.views import View as _View
from django.views.generic import CreateView as _CreateView
from django.views.generic import DeleteView as _DeleteView
from django.views.generic import DetailView as _DetailView
from django.views.generic import FormView as _FormView
from django.views.generic import ListView as _ListView
from django.views.generic import TemplateView as _TemplateView
from django.views.generic import UpdateView as _UpdateView


# View and the generic aliases stay importable via __getattr__ (with a
# DeprecationWarning); keep them out of __all__ so `import *` skips them.
__all__ = ["StaticView"]


class _DeprecatedView(_View):
    """Deprecated base view that runs ``after_view_process`` on every response.

    Superseded by Django's own views; kept working through django-boost 3.x and
    removed in 4.0. It re-implements ``as_view`` and does not support async
    handlers. Prefer a ``dispatch()`` override or middleware.
    """

    @classonlymethod
    def as_view(cls, **initkwargs):
        # Reuse Django's as_view for initkwargs validation and to capture the
        # attributes it sets on the view callable (view_class, decorator
        # markers such as csrf_exempt, ...); only the dispatch call is wrapped.
        native = super().as_view(**initkwargs)

        def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            self.setup(request, *args, **kwargs)
            if not hasattr(self, 'request'):
                raise AttributeError(
                    "%s instance has no 'request' attribute. Did you override "
                    "setup() and forget to call super()?" % cls.__name__
                )
            response = self.dispatch(request, *args, **kwargs)
            return self.after_view_process(request, response, *args, **kwargs)

        update_wrapper(view, native)
        return view

    def after_view_process(self, request, response, *args, **kwargs):
        return response


_DEPRECATED = {
    "View": _DeprecatedView,
    "TemplateView": type("TemplateView", (_DeprecatedView, _TemplateView), {}),
    "FormView": type("FormView", (_DeprecatedView, _FormView), {}),
    "CreateView": type("CreateView", (_DeprecatedView, _CreateView), {}),
    "ListView": type("ListView", (_DeprecatedView, _ListView), {}),
    "DetailView": type("DetailView", (_DeprecatedView, _DetailView), {}),
    "UpdateView": type("UpdateView", (_DeprecatedView, _UpdateView), {}),
    "DeleteView": type("DeleteView", (_DeprecatedView, _DeleteView), {}),
}


def __getattr__(name):
    if name in _DEPRECATED:
        warnings.warn(
            "django_boost.views.%s is deprecated and will be removed in "
            "django-boost 4.0; use django.views.generic.%s instead. The "
            "after_view_process hook is dropped; use a dispatch() override or "
            "middleware. (This view does not support async handlers.)"
            % (name, name),
            DeprecationWarning, stacklevel=2,
        )
        return _DEPRECATED[name]
    raise AttributeError(
        "module %r has no attribute %r" % (__name__, name))


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

    def get(self, request, *args, **kwargs):
        try:
            return self.create_response()
        except FileNotFoundError:
            # A file present when the route was registered may be gone at
            # request time; serve 404 as Django's own static view does.
            raise Http404
