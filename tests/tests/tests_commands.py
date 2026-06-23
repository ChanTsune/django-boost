from django.core.management import call_command

from django_boost.test import TestCase


class TestDeleteMigrations(TestCase):

    def test_call_command(self):
       call_command('deletemigrations', 'tests')
