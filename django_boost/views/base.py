import mimetypes
import os
from functools import update_wrapper

from django.core.exceptions import ImproperlyConfigured
from django.http import FileResponse
from django.utils.decorators import classonlymethod
from django.views import View as _View
from django.views.generic import CreateView as _CreateView
from django.views.generic import DeleteView as _DeleteView
from django.views.generic import DetailView as _DetailView
from django.views.generic import FormView as _FormView
from django.views.generic import ListView as _ListView
from django.views.generic import TemplateView as _TemplateView
from django.views.generic import UpdateView as _UpdateView


__all__ = ["View", "TemplateView", "FormView", "CreateView",
           "ListView", "DetailView", "UpdateView", "DeleteView",
           "StaticView"]


class View(_View):
    """View that runs ``after_view_process`` on every dispatched response.

    The hook wraps the result of ``as_view``'s dispatch call rather than
    ``dispatch`` itself, so it still fires when a mixin earlier in the MRO
    short-circuits ``dispatch`` (e.g. a permission check that returns a 403
    without calling ``super().dispatch()``).
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


class TemplateView(View, _TemplateView):
    pass


class FormView(View, _FormView):
    pass


class CreateView(View, _CreateView):
    pass


class ListView(View, _ListView):
    pass


class DetailView(View, _DetailView):
    pass


class UpdateView(View, _UpdateView):
    pass


class DeleteView(View, _DeleteView):
    pass


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


class StaticView(StaticResponseMixin, View):

    def get(self, request, *args, **kwargs):
        return self.create_response()
