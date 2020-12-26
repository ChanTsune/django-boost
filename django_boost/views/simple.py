from django.http import HttpResponse
from django.views.generic import View

__all__ = ['StringView']


class ResponseContentMixin:
    """Simple HttpResponse mixin."""

    response_class = HttpResponse
    content_type = None
    content = b''

    def get_content(self, **kwargs):
        """
        Return HttpResponse content.

        Pass keyword arguments from the URLconf.
        """
        return self.content

    def content_to_response(self, content, **response_kwargs):
        """
        Return a response, using the `response_class` for this view, with
        the given context.

        Pass response_kwargs to the constructor of the response class.
        """
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            content=content,
            **response_kwargs
        )


class StringView(ResponseContentMixin, View):
    """
    Create simple string response from content.

    Pass keyword arguments from the URLconf to the context.

    ::

      from django_boost.views.simple import StringView

      class MyStringView(StringView):
          content = 'Hello World!'

      class MyDynamicStringView(StringView):

          def get_content(self, **kwargs):
              return 'Hello World!'

    """

    def get(self, request, *args, **kwargs):
        content = self.get_content(**kwargs)
        return self.content_to_response(content)
