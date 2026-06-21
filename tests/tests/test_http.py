from django_boost.http import STATUS_MESSAGES
from django_boost.test import TestCase


class TestStatusMessages(TestCase):

    def test_http_510_and_511_messages(self):
        self.assertEqual(STATUS_MESSAGES[510], 'Not Extended')
        self.assertEqual(STATUS_MESSAGES[511], 'Network Authentication Required')

    def test_unknown_status_message_falls_back_to_empty_string(self):
        self.assertEqual(STATUS_MESSAGES[509], '')
