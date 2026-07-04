Test
====

:synopsis: Test utilities in django-boost

``django_boost.test.TestCase`` extends Django's ``TestCase`` with assertions
for a response's status code.

::

  from django_boost.test import TestCase

  class MyViewTests(TestCase):
      def test_ok(self):
          response = self.client.get("/")
          self.assertStatusCodeEqual(response, 200)

Each assertion takes the response first and an optional ``msg`` shown on
failure. A failure points at the calling test, not at the assertion helper.


assertStatusCodeEqual
---------------------

Assert the response status code equals ``code``.

::

  self.assertStatusCodeEqual(response, 200)


assertStatusCodeNotEqual
------------------------

Assert the response status code does not equal ``code``.

::

  self.assertStatusCodeNotEqual(response, 500)


assertStatusCodeIn
------------------

Assert the response status code is one of ``codes``.

::

  self.assertStatusCodeIn(response, [301, 302])


assertStatusCodeNotIn
---------------------

Assert the response status code is none of ``codes``.

::

  self.assertStatusCodeNotIn(response, [401, 403])
