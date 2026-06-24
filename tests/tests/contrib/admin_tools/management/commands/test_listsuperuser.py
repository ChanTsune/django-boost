import csv
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError

from django_boost.test import TestCase


class TestListSuperUser(TestCase):

    def setUp(self):
        User = get_user_model()
        self.active_superuser = User.objects.create_superuser(
            email='admin@example.com', username='admin', password='password')
        self.inactive_superuser = User.objects.create_superuser(
            email='old-root@example.com', username='oldroot',
            password='password')
        self.inactive_superuser.is_active = False
        self.inactive_superuser.save()
        self.normal_user = User.objects.create_user(
            email='normal@example.com', username='normal', password='password')

    def _lines(self, stdout):
        return stdout.getvalue().splitlines()

    def test_text_format_has_audit_columns_header(self):
        stdout = StringIO()
        call_command('listsuperuser', stdout=stdout)
        self.assertEqual(
            self._lines(stdout)[0], 'email | active | staff | last_login')

    def test_lists_only_superusers(self):
        stdout = StringIO()
        call_command('listsuperuser', stdout=stdout)
        output = stdout.getvalue()
        self.assertIn('admin@example.com', output)
        self.assertNotIn('normal@example.com', output)

    def test_inactive_superuser_is_flagged_inactive(self):
        stdout = StringIO()
        call_command('listsuperuser', stdout=stdout)
        rows = [r for r in self._lines(stdout)
                if r.startswith('old-root@example.com')]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].split(' | ')[1], 'no')

    def test_never_logged_in_shows_never(self):
        stdout = StringIO()
        call_command('listsuperuser', stdout=stdout)
        row = [r for r in self._lines(stdout)
               if r.startswith('admin@example.com')][0]
        self.assertEqual(row.split(' | ')[3], '(never)')

    def test_non_staff_superuser_is_flagged_no(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            email='nonstaff-root@example.com', username='nonstaffroot',
            password='password')
        user.is_staff = False
        user.save()
        stdout = StringIO()
        call_command('listsuperuser', stdout=stdout)
        row = [r for r in self._lines(stdout)
               if r.startswith('nonstaff-root@example.com')][0]
        self.assertEqual(row.split(' | ')[2], 'no')

    def test_csv_format_is_parseable(self):
        stdout = StringIO()
        call_command('listsuperuser', '--format', 'csv', stdout=stdout)
        rows = list(csv.reader(StringIO(stdout.getvalue())))
        self.assertEqual(rows[0], ['email', 'active', 'staff', 'last_login'])
        by_email = {r[0]: r for r in rows[1:]}
        self.assertEqual(by_email['admin@example.com'][1], 'yes')
        self.assertEqual(by_email['old-root@example.com'][1], 'no')

    def test_tsv_format_uses_tab_delimiter(self):
        stdout = StringIO()
        call_command('listsuperuser', '--format', 'tsv', stdout=stdout)
        rows = list(csv.reader(StringIO(stdout.getvalue()), delimiter='\t'))
        self.assertEqual(rows[0], ['email', 'active', 'staff', 'last_login'])

    def test_unsupported_format_raises_command_error(self):
        with self.assertRaises(CommandError):
            call_command('listsuperuser', format='xml')
