import unittest

from django.http import HttpResponse

from django_boost.test import TestCase


class AssertStatusCodeTests(TestCase):

    def test_custom_msg_appears_in_failure(self):
        with self.assertRaises(AssertionError) as cm:
            self.assertStatusCodeEqual(HttpResponse(status=404), 200,
                                       msg="custom note")
        self.assertIn("custom note", str(cm.exception))

    def test_not_equal_custom_msg_appears_in_failure(self):
        with self.assertRaises(AssertionError) as cm:
            self.assertStatusCodeNotEqual(HttpResponse(status=200), 200,
                                          msg="custom note")
        self.assertIn("custom note", str(cm.exception))

    def test_helper_frame_hidden_from_failure_traceback(self):
        class Inner(TestCase):
            def runTest(inner):
                inner.assertStatusCodeEqual(HttpResponse(status=404), 200)

        result = unittest.TestResult()
        Inner().run(result)
        self.assertEqual(len(result.failures), 1)
        formatted = result.failures[0][1]
        self.assertNotIn("in assertStatusCodeEqual", formatted)
