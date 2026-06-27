from __future__ import annotations

from collections.abc import Iterable

from django.http.response import HttpResponseBase
from django.test import TestCase as DjangoTestCase


class TestCase(DjangoTestCase):

    def assertStatusCodeEqual(self, response: HttpResponseBase, code: int) -> None:
        self.assertEqual(response.status_code, code)

    def assertStatusCodeNotEqual(self, response: HttpResponseBase, code: int) -> None:
        self.assertNotEqual(response.status_code, code)

    def assertStatusCodeIn(self, response: HttpResponseBase, codes: Iterable[int]) -> None:
        self.assertIn(response.status_code, codes)
