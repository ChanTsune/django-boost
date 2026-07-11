"""View mixins for Django's ``django.views``."""

from __future__ import annotations

import json
from datetime import timedelta
from typing import Sequence

from django.conf import settings
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.views import RedirectURLMixin, redirect_to_login
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt

from django_boost.http import HttpResponseUnsupportedMediaType
from django_boost.user_agents import parse_user_agent


__all__ = ["CSRFExemptMixin", "DynamicRedirectMixin", "RedirectToDetailMixin",
           "AllowContentTypeMixin", "LimitedTermMixin", "JsonRequestMixin",
           "JsonResponseMixin", "AnonymousRequiredMixin",
           "ReAuthenticationRequiredMixin", "StaffMemberRequiredMixin",
           "SuperuserRequiredMixin", "ViewUserKwargsMixin", "UserAgentMixin"]


class CSRFExemptMixin:
    """Mixin that exempts the view's ``dispatch()`` from CSRF protection."""

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        return super().dispatch(request, *args, **kwargs)


class DynamicRedirectMixin(RedirectURLMixin):
    """Mixin that prefers the ``?next=``-style redirect target over ``success_url``."""

    success_url = None

    def get_success_url(self):  # noqa: D102
        url = self.get_redirect_url()
        return url or self.success_url or super().get_success_url()


class RedirectToDetailMixin:
    """Mixin that redirects to the object's detail view instead of a fixed ``success_url``."""

    success_url_name: str | None = None
    url_kwarg: str = 'pk'
    object_field_name: str = 'pk'

    def get_success_url(self):  # noqa: D102
        field = getattr(self.object, self.object_field_name)
        kw = {self.url_kwarg: field}
        return reverse(self.success_url_name, kwargs=kw)


class AllowContentTypeMixin:
    """Mixin to restrict content type at the time of access."""

    allowed_content_types: Sequence[str] | None = None
    strictly = True

    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        allow_types = self.get_allowed_content_types()
        if self.strictly and request.content_type not in allow_types:
            return HttpResponseUnsupportedMediaType('415 '
                                                    'Unsupported Media Type',
                                                    content_type='text/html')
        return super().dispatch(request, *args, **kwargs)

    def get_allowed_content_types(self):  # noqa: D102
        if self.allowed_content_types is None:
            return []
        return self.allowed_content_types


class LimitedTermMixin:
    """Restrict time to access mixin."""

    exception_class = Http404
    start_datetime = None
    end_datetime = None

    def get_start_datetime(self):  # noqa: D102
        return self.start_datetime

    def get_end_datetime(self):  # noqa: D102
        return self.end_datetime

    def is_allowed_term(self, access_datetime):
        """Return True if access_datetime falls within [start_datetime, end_datetime), either bound optional."""
        start_datetime = self.get_start_datetime()
        end_datetime = self.get_end_datetime()
        if end_datetime is start_datetime is None:
            return True
        if end_datetime is None and start_datetime:
            return start_datetime < access_datetime
        if start_datetime is None and end_datetime:
            return access_datetime < end_datetime
        return start_datetime < access_datetime < end_datetime

    def dispatch(self, request, *args, **kwargs):  # noqa: D102
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
        """Return the charset declared on the request, or ``self.encoding`` as fallback."""
        # Honor a charset declared on the request; fall back to the default.
        return self.request.content_params.get('charset') or self.encoding

    def __json(self):
        try:
            return json.loads(self.request.body.decode(self.get_encoding()))
        except (json.JSONDecodeError, UnicodeDecodeError, LookupError):
            # Unreadable body (bad charset or bytes) is treated like malformed JSON.
            return {}

    @property
    def json(self):
        """Lazily parse and cache the request body as JSON."""
        if hasattr(self, "_json"):
            return self._json
        setattr(self, "_json", self.__json())
        return self._json

    @json.setter
    def json(self, value):
        self._json = value


class JsonResponseMixin:
    """Mixin that renders the view's context as a JSON response."""

    response_class = JsonResponse
    extra_context = None

    def get_context_data(self, **kwargs):
        """Merge ``extra_context`` with the given kwargs into a fresh dict."""
        # Copy extra_context into a fresh dict; updating it in place would
        # mutate the shared class attribute and leak kwargs across requests.
        context = dict(self.extra_context or {})
        context.update(kwargs)
        return context

    def get(self, request, *args, **kwargs):  # noqa: D102
        return self.response_class(self.get_context_data())

    post = get
    put = post


class AnonymousRequiredMixin:
    """
    Require the user to be anonymous.

    The inverse of Django's ``LoginRequiredMixin``: redirect an already
    authenticated user away, e.g. from a login or sign-up page.

    ::

      from django.views.generic import TemplateView
      from django_boost.views.mixins import AnonymousRequiredMixin

      class SignUpView(AnonymousRequiredMixin, TemplateView):
          template_name = "sign_up.html"
          redirect_authenticated_url = "/dashboard/"

    ``redirect_authenticated_url`` is where an authenticated user is sent;
    when it is ``None`` it falls back to ``settings.LOGIN_REDIRECT_URL``.
    """

    redirect_authenticated_url = None

    def get_redirect_authenticated_url(self):  # noqa: D102
        return self.redirect_authenticated_url or settings.LOGIN_REDIRECT_URL

    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        if request.user.is_authenticated:
            return redirect(self.get_redirect_authenticated_url())
        return super().dispatch(request, *args, **kwargs)


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

    interval: int | timedelta | None = None
    logout = False

    def get_interval(self):
        """Return ``interval`` as a ``timedelta``, raising if it's unset."""
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
        """Return True if ``user`` last logged in more than ``delta`` ago."""
        if user.last_login is None:
            # Never recorded a login (last_login is nullable); require re-auth.
            return True
        return (user.last_login + delta) < now()

    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        delta = self.get_interval()
        if self.need_reauthentication(request.user, delta):
            if self.logout:
                # logout_then_login() dispatches to LogoutView, which only
                # accepts POST from Django 5.0 (GET logout was removed); call
                # auth_logout() directly so this works for any request method.
                auth_logout(request)

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

    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        if request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        if self.superuser and request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()


class SuperuserRequiredMixin(AccessMixin):
    """Request super user authority."""

    permission_denied_message = 'Only super user can access'

    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()


class ViewUserKwargsMixin:
    """Mixin that adds the current request's user to the form kwargs.

    Pairs with ``django_boost.forms.mixins.FormUserKwargsMixin``, which
    consumes the ``user`` kwarg on the form side.
    """

    def get_form_kwargs(self):  # noqa: D102
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class UserAgentMixin:
    """Mixin that swaps in a device-specific template based on the parsed user agent."""

    pc_template_name: str | None = None
    tablet_template_name: str | None = None
    mobile_template_name: str | None = None

    def setup(self, request, *args, **kwargs):  # noqa: D102
        super().setup(request, *args, **kwargs)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        self.request.user_agent = parse_user_agent(user_agent)

    def get_template_names(self):  # noqa: D102
        tmp = super().get_template_names()
        if self.request.user_agent.is_pc and self.pc_template_name:
            return [self.pc_template_name] + tmp
        if self.request.user_agent.is_tablet and self.tablet_template_name:
            return [self.tablet_template_name] + tmp
        if self.request.user_agent.is_mobile and self.mobile_template_name:
            return [self.mobile_template_name] + tmp
        return tmp
