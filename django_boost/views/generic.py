from django.urls import path, reverse

from django_boost.views.base import (
    CreateView, DeleteView, DetailView, FormView,
    ListView, StaticView, TemplateView, UpdateView, View)
from django_boost.views.mixins import JsonRequestMixin, JsonResponseMixin

__all__ = ["CreateView", "DeleteView", "DetailView",
           "FormView", "JsonView", "ListView", "TemplateView",
           "UpdateView", "View", "StaticView"]
__views__ = ["BaseModelCLUDViews", "ModelCRUDViews"]

__all__ += __views__


class JsonView(JsonRequestMixin, JsonResponseMixin, View):
    """Return JsonResponse view."""


class BaseModelCLUDViews:
    model = None
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

    def update(self, request, *args, **kwargs):
        view_kwargs = {'fields': '__all__',
                       'success_url': self.get_success_url(), }
        view = self._as_view(self.update_view, **view_kwargs)
        return view(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        view_kwargs = {'fields': '__all__',
                       'success_url': self.get_success_url(), }
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
    list_view = ListView
    create_view = CreateView
    detail_view = DetailView
    update_view = UpdateView
    delete_view = DeleteView
