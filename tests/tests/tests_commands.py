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

    @classmethod
    def tearDownClass(self):
        import os
        from shutil import rmtree
        from django.conf import settings

        for f in ['app_for_test']:
            fp = os.path.join(settings.BASE_DIR, f)
            if os.path.exists(fp):
                rmtree(fp)


class TestSupportHeroku(TestCase):

    def test_call_command(self):
        call_command('support_heroku')

    @classmethod
    def tearDownClass(self):
        import os
        from django.conf import settings

        for f in ['Procfile', 'runtime.txt', 'requirements.txt']:
            fp = os.path.join(settings.BASE_DIR, f)
            if os.path.exists(fp):
                os.remove(fp)
