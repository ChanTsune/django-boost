import json
from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (SuccessURLAllowedHostsMixin,
                                       logout_then_login, redirect_to_login)
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.http import is_safe_url
from django.utils.timezone import now
from user_agents import parse

from django_boost.http import HttpResponseUnsupportedMediaType


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

    def is_allowed_trem(self, access_datetime):
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
        if not self.is_allowed_trem(now()):
            raise self.exception_class
        return super().dispatch(request, *args, **kwargs)


class JsonRequestMixin(AllowContentTypeMixin):
    """Only allow json request mixin."""

    allowed_content_types = ["application/json"]
    strictly = False

    @cached_property
    def json(self):
        try:
            return json.loads(self.request.body.encode('utf-8'))
        except json.JSONDecodeError:
            return {}


class JsonResponseMixin:

    extra_response_data = {}

    def get_response_data(self, **kwargs):
        response_data = {}
        response_data.update(self.extra_response_data)
        response_data.update(kwargs)
        return response_data

    def get(self, request, *args, **kwargs):
        return JsonResponse(self.get_response_data())


class ReAuthenticationRequiredMixin(LoginRequiredMixin):
    """Require authentication again on access."""

    auth_unnecessary = None
    logout = False

    def get_auth_unnecessary(self):
        if self.auth_unnecessary is None:
            return timedelta(seconds=0)
        if isinstance(self.auth_unnecessary, timedelta):
            return self.auth_unnecessary
        return timedelta(seconds=self.auth_unnecessary)

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)

        if response.status_code == 200:
            delta = self.get_auth_unnecessary()
            if now() > (request.user.last_login + delta):

                if self.logout:
                    return logout_then_login(request, self.get_login_url())

                return redirect_to_login(self.request.get_full_path(),
                                         self.get_login_url(),
                                         self.get_redirect_field_name())

        return response


class StaffMemberRequiredMixin(LoginRequiredMixin):
    """Request staff authority."""

    permission_denied_message = 'Only staff members can access'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()


class SuperuserRequiredMixin(LoginRequiredMixin):
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
        self.request.user_agent = parse(request.META['HTTP_USER_AGENT'])

    def get_template_names(self):
        tmp = super().get_template_names()
        if self.request.user_agent.is_pc and self.pc_template_name:
            return [self.pc_template_name] + tmp
        if self.request.user_agent.is_tablet and self.tablet_template_name:
            return [self.tablet_template_name] + tmp
        if self.request.user_agent.is_mobile and self.mobile_template_name:
            return [self.mobile_template_name] + tmp
        return tmp

