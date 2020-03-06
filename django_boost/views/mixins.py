import json
from datetime import timedelta

from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.views import (SuccessURLAllowedHostsMixin,
                                       logout_then_login, redirect_to_login)
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt

from django_boost.http import HttpResponseUnsupportedMediaType

from user_agents import parse


__all__ = ["CSRFExemptMixin", "DynamicRedirectMixin", "RedirectToDetailMixin",
           "AllowContentTypeMixin", "LimitedTermMixin", "JsonRequestMixin",
           "JsonResponseMixin", "ReAuthenticationRequiredMixin",
           "StaffMemberRequiredMixin", "SuperuserRequiredMixin",
           "ViewUserKwargsMixin", "UserAgentMixin"]


class CSRFExemptMixin:

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class DynamicRedirectMixin(SuccessURLAllowedHostsMixin):

    redirect_field_name = 'next'

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or super().get_success_url()

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        url_is_safe = is_safe_url(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''


class RedirectToDetailMixin:

    success_url_name = None
    url_kwarg = 'pk'
    object_field_name = 'pk'

    def get_success_url(self):
        field = getattr(self.object, self.object_field_name)
        kw = {self.url_kwarg: field}
        return reverse(self.success_url_name, kwargs=kw)


class AllowContentTypeMixin:
    """Mixin to restrict content type at the time of access."""

    allowed_content_types = None
    strictly = True

    def dispatch(self, request, *args, **kwargs):
        allow_types = self.get_allowed_content_types()
        if self.strictly and request.content_type not in allow_types:
            return HttpResponseUnsupportedMediaType('415 '
                                                    'Unsupported Media Type',
                                                    content_type='text/html')
        return super().dispatch(request, *args, **kwargs)

    def get_allowed_content_types(self):
        if self.allowed_content_types is None:
            return []
        return self.allowed_content_types


class LimitedTermMixin:
    """Restrict time to access mixin."""

    exception_class = Http404
    start_datetime = None
    end_datetime = None

    def get_start_datetime(self):
        return self.start_datetime

    def get_end_datetime(self):
        return self.end_datetime

    def is_allowed_term(self, access_datetime):
        start_datetime = self.get_start_datetime()
        end_datetime = self.get_end_datetime()
        if end_datetime is start_datetime is None:
            return True
        if end_datetime is None and start_datetime:
            return start_datetime < access_datetime
        if start_datetime is None and end_datetime:
            return access_datetime < end_datetime
        return start_datetime < access_datetime < end_datetime

    def dispatch(self, request, *args, **kwargs):
        if not self.is_allowed_term(now()):
            raise self.exception_class
        return super().dispatch(request, *args, **kwargs)


@method_decorator(csrf_exempt, name="dispatch")
class JsonRequestMixin(AllowContentTypeMixin):
    """Only allow json request mixin."""

    allowed_content_types = ["application/json"]
    strictly = False
    encoding = 'utf-8'

    def get_encoding(self):
        return self.encoding

    def __json(self):
        try:
            encoding = self.get_encoding()
            return json.loads(self.request.body.decode(encoding))
        except json.JSONDecodeError:
            return {}

    @property
    def json(self):
        if hasattr(self, "_json"):
            return self._json
        setattr(self, "_json", self.__json())
        return self._json

    @json.setter
    def json(self, value):
        self._json = value


class JsonResponseMixin:

    response_class = JsonResponse
    extra_context = None

    def get_context_data(self, **kwargs):
        context = self.extra_context or {}
        context.update(kwargs)
        return context

    def get(self, request, *args, **kwargs):
        return JsonResponse(self.get_context_data())

    post = get
    put = post


class ReAuthenticationRequiredMixin(AccessMixin):
    """
    Require authentication again on access.

    ::

      from django.views.generic import TemplateView
      from django_boost.views.mixins import ReAuthenticationRequiredMixin

      class RecentLoginView(ReAuthenticationRequiredMixin, TemplateView):
          template_name = "my_page.html"
          interval = 3600

    ::

      from datetime import timedelta
      from django.views.generic import TemplateView
      from django_boost.views.mixins import ReAuthenticationRequiredMixin

      class RecentLoginView(ReAuthenticationRequiredMixin,TemplateView):
          template_name = "my_page.html"
          interval = timedelta(hours=1)

    ``interval`` is the grace period until recertification.

    Can specify ``int`` or ``datetime.timedelta``.


    ``logout=True``, Logout if the specified time limit has passed.

    ``logout=False``, Do not logout Even if the specified time limit has passed.
    """

    interval = None
    logout = False

    def get_interval(self):
        if self.interval is None:
            raise ImproperlyConfigured(
                "%(cls)s is missing interval."
                "Set `interval` class variable "
                "or override `get_interval` method." % {
                    "cls": self.__class__.__name__
                }
            )
        if isinstance(self.interval, timedelta):
            return self.interval
        return timedelta(seconds=self.interval)

    def need_reauthentication(self, user, delta):
        return (user.last_login + delta) < now()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        delta = self.get_interval()
        if self.need_reauthentication(request.user, delta):

            if self.logout:
                return logout_then_login(request, self.get_login_url())

            return redirect_to_login(self.request.get_full_path(),
                                     self.get_login_url(),
                                     self.get_redirect_field_name())

        return super().dispatch(request, *args, **kwargs)


class StaffMemberRequiredMixin(AccessMixin):
    """
    Request staff authority.

    Set the class variable ``superuser`` to ``True`` to allow superuser.
    """

    permission_denied_message = 'Only staff members can access'
    superuser = False

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        if self.superuser and request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()


class SuperuserRequiredMixin(AccessMixin):
    """Request super user authority."""

    permission_denied_message = 'Only super user can access'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()


class ViewUserKwargsMixin:

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class UserAgentMixin:

    pc_template_name = None
    tablet_template_name = None
    mobile_template_name = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        self.request.user_agent = parse(user_agent)

    def get_template_names(self):
        tmp = super().get_template_names()
        if self.request.user_agent.is_pc and self.pc_template_name:
            return [self.pc_template_name] + tmp
        if self.request.user_agent.is_tablet and self.tablet_template_name:
            return [self.tablet_template_name] + tmp
        if self.request.user_agent.is_mobile and self.mobile_template_name:
            return [self.mobile_template_name] + tmp
        return tmp
