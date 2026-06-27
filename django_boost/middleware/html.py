from __future__ import annotations

from django.utils.deprecation import MiddlewareMixin

from django_boost.utils.html import (
    acompress_stream, compress_stream, strip_spaces_between_tags)


class SpaceLessMiddleware(MiddlewareMixin):
    """
    Middleware that remove white space in HTML.

    You will need to add the *SpaceLessMiddleware* to the MIDDLEWARE
    setting of your Django project *settings.py* file.

    ::

      MIDDLEWARE = [
          'django_boost.middleware.SpaceLessMiddleware',  # add
          'django.middleware.security.SecurityMiddleware',
          'django.contrib.sessions.middleware.SessionMiddleware',
          ...
      ]


    Install so that it is executed before middleware
    to compress such as GZipMiddleware.

    """

    def process_response(self, request, response):
        if 'text/html' in response.get('Content-Type', ''):
            if response.streaming:
                if response.is_async:
                    response.streaming_content = acompress_stream(
                        response.streaming_content, response.charset)
                else:
                    response.streaming_content = compress_stream(
                        response.streaming_content, response.charset)
                # Length is unknown until the lazily-compressed stream is sent.
                if response.has_header('Content-Length'):
                    del response['Content-Length']
            else:
                response.content = strip_spaces_between_tags(
                    response.content.decode(response.charset))
                response['Content-Length'] = str(len(response.content))
        return response
