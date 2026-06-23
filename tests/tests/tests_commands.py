from django.core.management import call_command

from django_boost.test import TestCase


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
