from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase, override_settings

from django_boost.http.response import (Http301, Http402, Http405, Http505,
                                         Http506, Http508, Http509, Http510,
                                         Http511)
from django_boost.middleware import (HttpStatusCodeExceptionMiddleware,
                                      RedirectCorrectHostnameMiddleware)


class HttpStatusCodeExceptionMiddlewareTests(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = HttpStatusCodeExceptionMiddleware(
            get_response=lambda request: HttpResponse())

    @override_settings(DEBUG=True)
    def test_renders_technical_page_when_debug(self):
        """With DEBUG on, a status-code exception renders the technical page."""
        response = self.middleware.process_exception(
            self.factory.get("/"), Http402())

        self.assertEqual(response.status_code, 402)
        content = response.content.decode()
        self.assertIn("Payment Required", content)
        self.assertIn("(402)", content)
        # Text unique to boost/technical/base.html, so it confirms the DEBUG
        # branch was taken rather than the production fallback.
        self.assertIn("DEBUG = True", content)

    @override_settings(DEBUG=False)
    def test_falls_back_to_plain_text_without_a_status_template(self):
        """In production with no `<code>.html` template, return a status line."""
        response = self.middleware.process_exception(
            self.factory.get("/"), Http402())

        self.assertEqual(response.status_code, 402)
        self.assertEqual(response.content.decode(), "402 Payment Required")

    @override_settings(DEBUG=False)
    def test_tail_5xx_exceptions_map_to_their_response(self):
        cases = [
            (Http505(), 505, "505 HTTP Version Not Supported"),
            (Http506(), 506, "506 Variant Also Negotiates"),
            (Http508(), 508, "508 Loop Detected"),
            (Http509(), 509, "509 Bandwidth Limit Exceeded"),
            (Http510(), 510, "510 Not Extended"),
            (Http511(), 511, "511 Network Authentication Required"),
        ]
        for exc, code, body in cases:
            with self.subTest(code=code):
                response = self.middleware.process_exception(
                    self.factory.get("/"), exc)
                self.assertEqual(response.status_code, code)
                self.assertEqual(response.content.decode(), body)

    def test_redirect_exception_becomes_a_redirect_response(self):
        response = self.middleware.process_exception(
            self.factory.get("/"), Http301("/moved"))

        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], "/moved")

    def test_unrelated_exception_is_not_handled(self):
        self.assertIsNone(self.middleware.process_exception(
            self.factory.get("/"), ValueError()))

    @override_settings(DEBUG=False)
    def test_method_not_allowed_sets_allow_and_keeps_body(self):
        response = self.middleware.process_exception(
            self.factory.get("/"), Http405(["GET", "POST"]))

        self.assertEqual(response.status_code, 405)
        self.assertEqual(response["Allow"], "GET, POST")
        self.assertEqual(response.content.decode(), "405 Method Not Allowed")

    @override_settings(DEBUG=False)
    def test_method_not_allowed_without_methods_has_empty_allow(self):
        response = self.middleware.process_exception(
            self.factory.get("/"), Http405())

        self.assertEqual(response.status_code, 405)
        self.assertEqual(response["Allow"], "")
        self.assertEqual(response.content.decode(), "405 Method Not Allowed")

    @override_settings(DEBUG=True)
    def test_method_not_allowed_does_not_crash_in_debug(self):
        response = self.middleware.process_exception(
            self.factory.get("/"), Http405(["GET"]))

        self.assertEqual(response.status_code, 405)
        self.assertEqual(response["Allow"], "GET")
        self.assertIn("Method Not Allowed", response.content.decode())


class RedirectCorrectHostnameMiddlewareTests(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.downstream = []

    def _middleware(self):
        def get_response(request):
            self.downstream.append(request)
            return HttpResponse()
        return RedirectCorrectHostnameMiddleware(get_response)

    @override_settings(DEBUG=False, CORRECT_HOST="correct.example.com",
                       ALLOWED_HOSTS=["*"])
    def test_redirects_when_hostname_differs(self):
        response = self._middleware()(
            self.factory.get("/page?x=1", HTTP_HOST="wrong.example.com"))

        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"],
                         "http://correct.example.com/page?x=1")
        self.assertEqual(self.downstream, [])  # not forwarded to the view

    @override_settings(DEBUG=False, CORRECT_HOST="correct.example.com",
                       ALLOWED_HOSTS=["*"])
    def test_no_redirect_when_hostname_matches(self):
        response = self._middleware()(
            self.factory.get("/", HTTP_HOST="correct.example.com"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.downstream), 1)

    @override_settings(DEBUG=True, CORRECT_HOST="correct.example.com",
                       ALLOWED_HOSTS=["*"])
    def test_no_redirect_when_debug(self):
        response = self._middleware()(
            self.factory.get("/", HTTP_HOST="wrong.example.com"))

        self.assertEqual(response.status_code, 200)

    def _async_middleware(self):
        async def get_response(request):
            self.downstream.append(request)
            return HttpResponse()
        return RedirectCorrectHostnameMiddleware(get_response)

    @override_settings(DEBUG=False, CORRECT_HOST="correct.example.com",
                       ALLOWED_HOSTS=["*"])
    async def test_redirects_when_hostname_differs_async(self):
        """Under ASGI (async get_response) the redirect path must not crash."""
        response = await self._async_middleware()(
            self.factory.get("/page?x=1", HTTP_HOST="wrong.example.com"))

        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"],
                         "http://correct.example.com/page?x=1")
        self.assertEqual(self.downstream, [])  # not forwarded to the view

    @override_settings(DEBUG=False, CORRECT_HOST="correct.example.com",
                       ALLOWED_HOSTS=["*"])
    async def test_no_redirect_when_hostname_matches_async(self):
        response = await self._async_middleware()(
            self.factory.get("/", HTTP_HOST="correct.example.com"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.downstream), 1)
