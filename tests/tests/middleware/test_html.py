from django.http import StreamingHttpResponse
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
