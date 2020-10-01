from django_boost.test import TestCase
from django.core.management import call_command


class TestAdminSiteLog(TestCase):

    def test_call_command(self):
        call_command('adminsitelog')


class TestDeleteMigrations(TestCase):

    def test_call_command(self):
       call_command('deletemigrations', 'tests')


class TestStartAppPlus(TestCase):

    def test_call_command(self):
        call_command('startapp_plus', 'app_for_test')


class TestSupportHeroku(TestCase):

    def test_call_command(self):
        call_command('support_heroku')
