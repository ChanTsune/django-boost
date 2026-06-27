import warnings

from django.http import HttpResponse

from django_boost.views.mixins import AllowContentTypeMixin
from django_boost.views.simple import StringView

# These fixtures intentionally exercise the deprecated View / after_view_process
# (still functional in 3.x); suppress the warning at import so the suite stays clean.
with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    from django_boost.views.base import TemplateView, View


class SimpleStringView(StringView):
    content = b'test string'


class DynamicStringView(StringView):

    def get_content(self, **kwargs):
        return str(kwargs)


class AfterViewProcessView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse("processed")

    def after_view_process(self, request, response, *args, **kwargs):
        response["X-After-View-Process"] = "yes"
        return response


class ShortCircuitAfterViewProcessView(AllowContentTypeMixin, View):
    """A short-circuiting mixin precedes View, so dispatch never reaches it."""

    allowed_content_types = ["application/json"]

    def get(self, request, *args, **kwargs):
        return HttpResponse("processed")

    def after_view_process(self, request, response, *args, **kwargs):
        response["X-After-View-Process"] = "yes"
        return response


class GenericAfterViewProcessView(TemplateView):
    template_name = "boost/test/index.html"

    def after_view_process(self, request, response, *args, **kwargs):
        response["X-After-View-Process"] = "yes"
        return response
