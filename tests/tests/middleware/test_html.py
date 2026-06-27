import asyncio

from django.http import HttpResponse, StreamingHttpResponse
from django.test import RequestFactory, SimpleTestCase

from django_boost.middleware.html import SpaceLessMiddleware


class SpaceLessMiddlewareStreamingTests(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_streaming_response_is_compressed_lazily(self):
        consumed = []

        def gen():
            consumed.append(True)
            yield b'<html>  <body>  hi  </body>  </html>'

        def get_response(request):
            return StreamingHttpResponse(gen(), content_type='text/html')

        response = SpaceLessMiddleware(get_response)(self.factory.get('/'))

        self.assertEqual(consumed, [])
        self.assertEqual(b''.join(response.streaming_content),
                         b'<html><body>hi</body></html>')

    def test_streaming_compresses_across_chunk_boundaries(self):
        def gen():
            yield b'<html>  <bo'
            yield b'dy>  hi  </body'
            yield b'>  </html>'

        def get_response(request):
            return StreamingHttpResponse(gen(), content_type='text/html')

        response = SpaceLessMiddleware(get_response)(self.factory.get('/'))

        self.assertEqual(b''.join(response.streaming_content),
                         b'<html><body>hi</body></html>')

    def test_async_streaming_response_is_compressed(self):
        async def agen():
            yield b'<html>  <body>  hi  </body>  </html>'

        def get_response(request):
            return StreamingHttpResponse(agen(), content_type='text/html')

        response = SpaceLessMiddleware(get_response)(self.factory.get('/'))
        self.assertTrue(response.streaming)

        async def collect():
            return b''.join([c async for c in response.streaming_content])

        self.assertEqual(asyncio.run(collect()),
                         b'<html><body>hi</body></html>')

    def test_async_streaming_response_is_not_consumed_eagerly(self):
        consumed = []

        async def agen():
            consumed.append(True)
            yield b'<html>  <body>  hi  </body>  </html>'

        def get_response(request):
            return StreamingHttpResponse(agen(), content_type='text/html')

        response = SpaceLessMiddleware(get_response)(self.factory.get('/'))

        self.assertEqual(consumed, [])

        async def collect():
            return b''.join([c async for c in response.streaming_content])

        self.assertEqual(asyncio.run(collect()), b'<html><body>hi</body></html>')
        self.assertEqual(consumed, [True])

    def test_async_streaming_handles_multibyte_split_across_chunks(self):
        body = '<html> <body>あい</body> </html>'.encode('utf-8')

        async def agen():
            yield body[:14]
            yield body[14:]

        def get_response(request):
            return StreamingHttpResponse(agen(), content_type='text/html')

        response = SpaceLessMiddleware(get_response)(self.factory.get('/'))

        async def collect():
            return b''.join([c async for c in response.streaming_content])

        self.assertEqual(asyncio.run(collect()).decode('utf-8'),
                         '<html><body>あい</body></html>')

    def test_streaming_drops_content_length(self):
        def get_response(request):
            response = StreamingHttpResponse([b'<html>  x  </html>'],
                                             content_type='text/html')
            response['Content-Length'] = '18'
            return response

        response = SpaceLessMiddleware(get_response)(self.factory.get('/'))

        self.assertFalse(response.has_header('Content-Length'))

    def test_streaming_handles_multibyte_split_across_chunks(self):
        body = '<html> <body>あい</body> </html>'.encode('utf-8')

        def gen():
            yield body[:14]
            yield body[14:]

        def get_response(request):
            return StreamingHttpResponse(gen(), content_type='text/html')

        response = SpaceLessMiddleware(get_response)(self.factory.get('/'))

        self.assertEqual(b''.join(response.streaming_content).decode('utf-8'),
                         '<html><body>あい</body></html>')


class SpaceLessMiddlewareAsyncChainTests(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_async_get_response_is_awaited(self):
        async def get_response(request):
            return HttpResponse('<html>  <body>  hi  </body>  </html>',
                                content_type='text/html')

        middleware = SpaceLessMiddleware(get_response)

        async def call():
            return await middleware(self.factory.get('/'))

        response = asyncio.run(call())

        self.assertEqual(response.content, b'<html><body>hi</body></html>')

    def test_async_get_response_streaming_is_compressed(self):
        async def agen():
            yield b'<html>  <bo'
            yield b'dy>  hi  </body'
            yield b'>  </html>'

        async def get_response(request):
            return StreamingHttpResponse(agen(), content_type='text/html')

        middleware = SpaceLessMiddleware(get_response)

        async def call():
            response = await middleware(self.factory.get('/'))
            return b''.join([c async for c in response.streaming_content])

        self.assertEqual(asyncio.run(call()), b'<html><body>hi</body></html>')


class SpaceLessMiddlewarePassthroughTests(SimpleTestCase):
    """Non-HTML responses must be left byte-for-byte untouched."""

    def setUp(self):
        self.factory = RequestFactory()

    def test_non_html_response_is_left_untouched(self):
        body = b'{"a":  1,  "b":  2}'  # whitespace must not be collapsed

        def get_response(request):
            return HttpResponse(body, content_type='application/json')

        response = SpaceLessMiddleware(get_response)(self.factory.get('/'))

        self.assertEqual(response.content, body)

    def test_non_html_streaming_response_is_left_untouched(self):
        chunks = [b'\x00\x01  \x02', b'  raw  bytes  ']

        def get_response(request):
            return StreamingHttpResponse(iter(chunks),
                                         content_type='application/octet-stream')

        response = SpaceLessMiddleware(get_response)(self.factory.get('/'))

        self.assertEqual(b''.join(response.streaming_content), b''.join(chunks))


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
