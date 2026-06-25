from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase, override_settings

from django_boost.http.response import Http301, Http402
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

    def test_redirect_exception_becomes_a_redirect_response(self):
        response = self.middleware.process_exception(
            self.factory.get("/"), Http301("/moved"))

        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], "/moved")

    def test_unrelated_exception_is_not_handled(self):
        self.assertIsNone(self.middleware.process_exception(
            self.factory.get("/"), ValueError()))


class RedirectCorrectHostnameMiddlewareTests(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @override_settings(CORRECT_HOST="correct.example.com", ALLOWED_HOSTS=["*"])
    def test_redirects_when_hostname_differs(self):
        downstream = []
        middleware = RedirectCorrectHostnameMiddleware(
            get_response=lambda request: downstream.append(request))
        # `conditions` is frozen at class-definition time (DEBUG was on then);
        # simulate a deployment where the redirect is active.
        middleware.conditions = True

        response = middleware(self.factory.get("/page?x=1"))

        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"],
                         "http://correct.example.com/page?x=1")
        self.assertEqual(downstream, [])  # not forwarded to the view

    def test_passes_through_when_disabled(self):
        sentinel = HttpResponse()
        middleware = RedirectCorrectHostnameMiddleware(
            get_response=lambda request: sentinel)
        # Default `conditions` is False under the test settings (DEBUG on), so
        # the request flows through untouched.
        self.assertIs(middleware(self.factory.get("/")), sentinel)
