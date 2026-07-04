from django_boost.http import STATUS_MESSAGES
from django_boost.http.response import (Http505, Http506, Http508, Http509,
                                        Http510, Http511)
from django_boost.test import TestCase


class TestStatusMessages(TestCase):

    def test_http_509_510_511_messages(self):
        self.assertEqual(STATUS_MESSAGES[509], 'Bandwidth Limit Exceeded')
        self.assertEqual(STATUS_MESSAGES[510], 'Not Extended')
        self.assertEqual(STATUS_MESSAGES[511], 'Network Authentication Required')

    def test_unknown_status_message_falls_back_to_empty_string(self):
        self.assertEqual(STATUS_MESSAGES[512], '')


class TestHttp5xxTailExceptions(TestCase):
    """The 5xx exceptions whose response classes already exist can be raised."""

    def test_tail_exceptions_expose_their_status_code(self):
        cases = [(Http505, 505), (Http506, 506), (Http508, 508),
                 (Http509, 509), (Http510, 510), (Http511, 511)]
        for exc, code in cases:
            with self.subTest(exc.__name__):
                self.assertEqual(exc().status_code, code)
                self.assertEqual(exc.response_class.status_code, code)


class TestHttpPackageReExportsExceptions(TestCase):
    """Every status-code exception is importable from ``django_boost.http``.

    Mirrors Django's own ``Http404``, which is importable from ``django.http``.
    Derived from the classes in ``response`` so a newly added exception is
    covered without editing this test.
    """

    def _status_exception_names(self):
        from django_boost.http import response
        bases = (response.HttpExceptionBase,
                 response.HttpRedirectExceptionBase)
        return [name for name, obj in vars(response).items()
                if isinstance(obj, type)
                and issubclass(obj, response.HttpExceptionBase)
                and obj not in bases]

    def test_status_exceptions_importable_from_package(self):
        from django_boost import http
        from django_boost.http import response
        for name in self._status_exception_names():
            with self.subTest(name):
                self.assertIs(getattr(http, name, None),
                              getattr(response, name))

    def test_status_exceptions_listed_in_all(self):
        from django_boost import http
        for name in self._status_exception_names():
            with self.subTest(name):
                self.assertIn(name, http.__all__)
