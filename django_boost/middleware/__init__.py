"""Middleware extensions for Django's request/response cycle."""

from __future__ import annotations

from django.conf import settings
from django.http import HttpRequest, HttpResponseBase, HttpResponsePermanentRedirect
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template
from django.utils.deprecation import MiddlewareMixin

from django_boost.http import STATUS_MESSAGES
from django_boost.http.response import (
    Http405,
    HttpExceptionBase,
    HttpRedirectExceptionBase
)

from .html import SpaceLessMiddleware


__all__ = ['SpaceLessMiddleware',
           'RedirectCorrectHostnameMiddleware',
           'HttpStatusCodeExceptionMiddleware']


class RedirectCorrectHostnameMiddleware(MiddlewareMixin):
    """
    Redirect to correct hostname.

    if requested hostname and settings.CORRECT_HOST does not match.

    You will need to add the *RedirectCorrectHostnameMiddleware* to the MIDDLEWARE
    setting of your Django project *settings.py* file.

    ::

      MIDDLEWARE = [
          'django_boost.middleware.RedirectCorrectHostnameMiddleware',  # add
          'django.middleware.security.SecurityMiddleware',
          'django.contrib.sessions.middleware.SessionMiddleware',
          ...
      ]

    CORRECT_HOST = 'sample.com'


    Redirect all access to the domain specified in ``CORRECT_HOST``

    It is not redirected when ``DEBUG = True``

    This is useful when migrating domains

    Originally it should be done with server software such as nginx and apache,

    but it is useful when the setting is troublesome or when using services such as heroku.
    """

    def process_request(self, request: HttpRequest) -> HttpResponsePermanentRedirect | None:  # noqa: D102
        # Return the redirect from process_request rather than overriding
        # __call__, so MiddlewareMixin's own __call__/__acall__ short-circuit
        # correctly under both WSGI and ASGI. A synchronous __call__ override
        # would return a bare HttpResponse on the async path, which Django then
        # awaits -> TypeError.
        correct_host = getattr(settings, 'CORRECT_HOST', None)
        enabled = not settings.DEBUG and correct_host
        if enabled and request.get_host() != correct_host:
            return HttpResponsePermanentRedirect(
                '{scheme}://{host}{path}'.format(scheme=request.scheme,
                                                 host=correct_host,
                                                 path=request.get_full_path()))
        return None


class HttpStatusCodeExceptionMiddleware(MiddlewareMixin):
    """
    Handle status code exceptions.

    similar to the `Http404` exception.

    You will need to add the *HttpStatusCodeExceptionMiddleware* to the MIDDLEWARE
    setting of your Django project *settings.py* file.

    ::

      MIDDLEWARE = [
          'django_boost.middleware.HttpStatusCodeExceptionMiddleware',  # add
          'django.middleware.security.SecurityMiddleware',
          'django.contrib.sessions.middleware.SessionMiddleware',
          ...
      ]

    This Middleware is required when using the :doc:`http_status_code_exceptions`.

    """

    def get_template_from_status_code(self, status_code: int, request: HttpRequest | None = None) -> str:
        """Render the status page template for ``status_code``, falling back to a plain-text message."""
        message = STATUS_MESSAGES[status_code]
        try:
            if settings.DEBUG:
                file_name = "boost/technical/base.html"
            else:
                file_name = "%s.html" % status_code
            t = get_template(file_name)
            context = {'status_code': status_code,
                       'status_message': message}
            return t.render(context, request)
        except TemplateDoesNotExist:
            return "%s %s" % (status_code, message)

    def process_exception(self, request: HttpRequest, e: Exception) -> HttpResponseBase | None:
        """Turn an ``HttpExceptionBase`` into its response, or a redirect for ``HttpRedirectExceptionBase``."""
        if isinstance(e, HttpRedirectExceptionBase):
            return e.response_class(e.url)
        elif isinstance(e, HttpExceptionBase):
            response_text = self.get_template_from_status_code(
                e.status_code, request)
            if isinstance(e, Http405):
                # HttpResponseNotAllowed takes the allowed methods first, not
                # the body.
                return e.response_class(e.permitted_methods,
                                        content=response_text)
            return e.response_class(response_text)
        return None
