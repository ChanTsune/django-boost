"""The ``SpaceLessMiddleware`` HTML-whitespace-compressing middleware."""

from __future__ import annotations

from collections.abc import AsyncIterable, Iterable
from typing import cast

from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBase,
    StreamingHttpResponse,
)
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

    def process_response(
            self, request: HttpRequest,
            response: HttpResponseBase) -> HttpResponseBase:
        if 'text/html' in response.get('Content-Type', ''):
            if response.streaming:
                # streaming is only True for StreamingHttpResponse, which is
                # what exposes is_async / streaming_content.
                streaming = cast(StreamingHttpResponse, response)
                if streaming.is_async:
                    streaming.streaming_content = acompress_stream(
                        cast(AsyncIterable[bytes],
                             streaming.streaming_content),
                        response.charset)
                else:
                    streaming.streaming_content = compress_stream(
                        cast(Iterable[bytes], streaming.streaming_content),
                        response.charset)
                # Length is unknown until the lazily-compressed stream is sent.
                if response.has_header('Content-Length'):
                    del response['Content-Length']
            else:
                full = cast(HttpResponse, response)
                full.content = strip_spaces_between_tags(
                    full.content.decode(response.charset))
                full['Content-Length'] = str(len(full.content))
        return response
