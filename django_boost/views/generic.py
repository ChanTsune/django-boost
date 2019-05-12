from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.utils.translation import gettext as _
from django.views.generic import View

from django_boost.views.mixins import JsonRequestMixin, JsonResponseMixin


class JsonView(JsonRequestMixin, JsonResponseMixin, View):
    """Return JsonResponse view."""


