from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.template import Context
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template
from django.utils.deprecation import MiddlewareMixin

from django_boost.http.response import HttpExceptionBase


class RedirectCorrectHostnameMiddleware(MiddlewareMixin):
    """
    Redirect to correct hostname.

    if requested hostname and settings.CORRECT_HOST does not match.
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
    """

    def get_template_from_status_code(self, status_code):
        try:
            file_name = "%s.html" % status_code
            t = get_template(file_name)
            context = Context()
            return t.render(context)
        except TemplateDoesNotExist:
            return "%s" % status_code

    def process_exception(self, request, e):
        if isinstance(e, HttpExceptionBase):
            response_text = self.get_template_from_status_code(e.status_code)
            return e.response_class(response_text)
        return None
