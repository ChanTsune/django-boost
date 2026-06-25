from django.http import HttpResponse, StreamingHttpResponse
from django.test import RequestFactory, SimpleTestCase

from django_boost.middleware.html import SpaceLessMiddleware


class SpaceLessMiddlewareStreamingTests(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_compresses_streaming_html_response(self):
        def get_response(request):
            return StreamingHttpResponse(
                [b'<html>  <body>  hi  </body>  </html>'],
                content_type='text/html')

        middleware = SpaceLessMiddleware(get_response)
        response = middleware(self.factory.get('/'))

        self.assertTrue(response.streaming)
        self.assertEqual(b''.join(response.streaming_content),
                         b'<html><body>hi</body></html>')


class SpaceLessMiddlewareCharsetTests(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_compresses_non_utf8_html_response(self):
        html = '<html> <body>café</body> </html>'

        def get_response(request):
            return HttpResponse(html.encode('latin-1'),
                                content_type='text/html; charset=latin-1')

        middleware = SpaceLessMiddleware(get_response)
        response = middleware(self.factory.get('/'))

        self.assertEqual(response.content.decode('latin-1'),
                         '<html><body>café</body></html>')
