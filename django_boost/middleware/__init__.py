from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template
from django.utils.deprecation import MiddlewareMixin

from django_boost.http import STATUS_MESSAGES
from django_boost.http.response import (HttpExceptionBase,
                                        HttpRedirectExceptionBase)
from django_boost.middleware.html import SpaceLessMiddleware


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

    Originally it should be done with server software such as nginx and apache, but it is useful when the setting is troublesome or when using services such as heroku
    """

    conditions = not settings.DEBUG and hasattr(settings, 'CORRECT_HOST')

    def __call__(self, request):

        if self.conditions and request.get_host() != settings.CORRECT_HOST:
            return HttpResponsePermanentRedirect(
                '{scheme}://{host}{path}'.format(scheme=request.scheme,
                                                 host=settings.CORRECT_HOST,
                                                 path=request.get_full_path()))

        response = self.get_response(request)
        return response


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

    def get_template_from_status_code(self, status_code, request=None):
        message = STATUS_MESSAGES[status_code]
        try:
            if settings.DEBUG:
                file_name = "boost/tecnical/base.html"
            else:
                file_name = "%s.html" % status_code
            t = get_template(file_name)
            context = {'status_code': status_code,
                       'status_message': message}
            return t.render(context, request)
        except TemplateDoesNotExist:
            return "%s %s" % (status_code, message)

    def process_exception(self, request, e):
        if isinstance(e, HttpRedirectExceptionBase):
            return e.response_class(e.url)
        elif isinstance(e, HttpExceptionBase):
            response_text = self.get_template_from_status_code(
                e.status_code, request)
            return e.response_class(response_text)
        return None
