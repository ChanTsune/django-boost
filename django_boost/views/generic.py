"""Extensions for Django's ``django.views.generic``."""

from __future__ import annotations

import warnings

from django.db import models
from django.urls import path, reverse
from django.views import View as _View
from django.views.generic import CreateView as _CreateView
from django.views.generic import DeleteView as _DeleteView
from django.views.generic import DetailView as _DetailView
from django.views.generic import ListView as _ListView
from django.views.generic import UpdateView as _UpdateView

from django_boost.views.base import StaticView
from django_boost.views.base import _DEPRECATED as _DEPRECATED_VIEWS
from django_boost.views.mixins import JsonRequestMixin, JsonResponseMixin

# View and the generic aliases stay importable via __getattr__ (with a
# DeprecationWarning); keep them out of __all__ so `import *` skips them.
__all__ = ["JsonView", "StaticView"]
__views__ = ["BaseModelCLUDViews", "ModelCRUDViews"]

__all__ += __views__


def __getattr__(name):
    if name in _DEPRECATED_VIEWS:
        warnings.warn(
            "django_boost.views.generic.%s is deprecated and will be removed "
            "in django-boost 4.0; use django.views.generic.%s instead. The "
            "after_view_process hook is dropped; use a dispatch() override or "
            "middleware. (This view does not support async handlers.)"
            % (name, name),
            DeprecationWarning, stacklevel=2,
        )
        return _DEPRECATED_VIEWS[name]
    raise AttributeError(
        "module %r has no attribute %r" % (__name__, name))


class JsonView(JsonRequestMixin, JsonResponseMixin, _View):
    """
    JsonResponse view.

    A generic view class that inherits ``JsonResponseMixin`` and ``JsonRequestMixin``.

    ::

      from django_boost.views.generic import JsonView

      class SameAPIView(JsonView):

          def get_context_data(self, **kwargs):
              return self.json

    In the above example, we just return the sent Json string as it is.

    """


class BaseModelCLUDViews:
    model: type[models.Model] | None = None
    success_url = None
    list_view = None
    create_view = None
    detail_view = None
    update_view = None
    delete_view = None
    list_url_pattern = ''
    create_url_pattern = 'create/'
    detail_url_pattern = '<int:pk>/'
    update_url_pattern = '<int:pk>/update/'
    delete_url_pattern = '<int:pk>/delete/'
    success_url = None

    def __init__(self, app_name=None):
        """Fall back to the model's lowercased class name when ``app_name`` is omitted."""
        if self.model:
            model_name = self.model.__name__.lower()
        else:
            model_name = None
        self.app_name = app_name or model_name

    def get_success_url(self):
        if self.success_url is None:
            return reverse('%s:list' % self.app_name)
        return self.success_url

    def _as_view(self, view_class, **kwargs):
        kwargs.update({'model': self.model})
        return view_class.as_view(**kwargs)

    def _form_view_kwargs(self, view_class):
        # Default fields='__all__' only when the view has no form_class/fields
        # of its own (fields + form_class is ImproperlyConfigured).
        view_kwargs = {'success_url': self.get_success_url()}
        if not getattr(view_class, 'form_class', None) and not getattr(view_class, 'fields', None):
            view_kwargs['fields'] = '__all__'
        return view_kwargs

    def update(self, request, *args, **kwargs):
        view_kwargs = self._form_view_kwargs(self.update_view)
        view = self._as_view(self.update_view, **view_kwargs)
        return view(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        view_kwargs = self._form_view_kwargs(self.create_view)
        view = self._as_view(self.create_view, **view_kwargs)
        return view(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        view_kwargs = {'success_url': self.get_success_url(), }
        view = self._as_view(self.delete_view, **view_kwargs)
        return view(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        view_kwargs = {}
        view = self._as_view(self.list_view, **view_kwargs)
        return view(request, *args, **kwargs)

    def detail(self, request, *args, **kwargs):
        view_kwargs = {}
        view = self._as_view(self.detail_view, **view_kwargs)
        return view(request, *args, **kwargs)

    def get_urls(self):
        urlpatterns = []
        if self.list_view:
            urlpatterns += [path(self.list_url_pattern,
                                 self.list, name='list')]
        if self.create_view:
            urlpatterns += [path(self.create_url_pattern,
                                 self.create, name='create')]
        if self.detail_view:
            urlpatterns += [path(self.detail_url_pattern,
                                 self.detail, name='detail')]
        if self.update_view:
            urlpatterns += [path(self.update_url_pattern,
                                 self.update, name='update')]
        if self.delete_view:
            urlpatterns += [path(self.delete_url_pattern,
                                 self.delete, name='delete')]
        return urlpatterns

    @property
    def urls(self):
        return (self.get_urls(), self.app_name)


class ModelCRUDViews(BaseModelCLUDViews):
    list_view = _ListView
    create_view = _CreateView
    detail_view = _DetailView
    update_view = _UpdateView
    delete_view = _DeleteView
