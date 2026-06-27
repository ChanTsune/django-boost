from __future__ import annotations

from collections.abc import Iterable

from django.http.response import HttpResponseBase
from django.test import TestCase as DjangoTestCase

# Hide this module's frames from assertion tracebacks (the convention unittest
# itself uses in unittest/case.py) so a failed assertStatusCode* points at the
# calling test rather than at these helpers.
__unittest = True


class TestCase(DjangoTestCase):

    def assertStatusCodeEqual(self, response: HttpResponseBase, code: int,
                              msg: object = None) -> None:
        self.assertEqual(response.status_code, code, msg)

    def assertStatusCodeNotEqual(self, response: HttpResponseBase, code: int,
                                 msg: object = None) -> None:
        self.assertNotEqual(response.status_code, code, msg)

    def assertStatusCodeIn(self, response: HttpResponseBase,
                           codes: Iterable[int], msg: object = None) -> None:
        self.assertIn(response.status_code, codes, msg)
