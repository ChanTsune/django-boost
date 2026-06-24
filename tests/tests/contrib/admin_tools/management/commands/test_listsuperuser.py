from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command

from django_boost.test import TestCase


class TestListSuperUser(TestCase):

    def setUp(self):
        User = get_user_model()
        self.superuser = User.objects.create_superuser(
            email='super@example.com',
            username='super',
            password='password')
        self.normal_user = User.objects.create_user(
            email='normal@example.com',
            username='normal',
            password='password')

    def test_call_command_lists_only_superusers(self):
        stdout = StringIO()

        call_command('listsuperuser', stdout=stdout)

        lines = stdout.getvalue().splitlines()
        self.assertIn(str(self.superuser), lines)
        self.assertNotIn(str(self.normal_user), lines)

    def test_call_command_lists_every_superuser(self):
        other_superuser = get_user_model().objects.create_superuser(
            email='super2@example.com',
            username='super2',
            password='password')
        stdout = StringIO()

        call_command('listsuperuser', stdout=stdout)

        lines = stdout.getvalue().splitlines()
        self.assertIn(str(self.superuser), lines)
        self.assertIn(str(other_superuser), lines)
