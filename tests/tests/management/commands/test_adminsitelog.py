import csv
from io import StringIO

from django.contrib.admin.models import ADDITION, CHANGE, LogEntry
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.core.management.base import CommandError

from django_boost.test import TestCase
from tests.models import RelatedItemModel


class TestAdminSiteLog(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='admin@example.com',
            username='admin',
            password='password')
        self.content_type = ContentType.objects.get_for_model(
            RelatedItemModel)
        self.log = LogEntry.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id='1',
            object_repr='Item, with comma',
            action_flag=ADDITION,
            change_message='')

    def test_call_command_with_text_format(self):
        stdout = StringIO()

        call_command('adminsitelog', '--no-color', stdout=stdout)

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], 'id | action | detail | user | time')
        self.assertTrue(lines[1].startswith(
            '%s | Added | Item, with comma | admin | ' % self.log.id))

    def test_call_command_with_changed_action(self):
        changed_log = LogEntry.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id='1',
            object_repr='Customer object',
            action_flag=CHANGE,
            change_message='Changed color.')
        stdout = StringIO()

        call_command('adminsitelog', '--format', 'csv', stdout=stdout)

        rows = {row[0]: row for row in csv.reader(StringIO(stdout.getvalue()))}
        row = rows[str(changed_log.id)]
        self.assertEqual(row[1], 'Changed')
        self.assertEqual(row[2], 'Customer object - Changed color.')

    def test_call_command_with_csv_format(self):
        stdout = StringIO()

        call_command('adminsitelog', '--format', 'csv', stdout=stdout)

        rows = list(csv.reader(StringIO(stdout.getvalue())))
        self.assertEqual(
            rows[0],
            ['id', 'action', 'detail', 'user', 'time'])
        self.assertEqual(rows[1][0], str(self.log.id))
        self.assertEqual(rows[1][1], 'Added')
        self.assertEqual(rows[1][2], 'Item, with comma')
        self.assertEqual(rows[1][3], 'admin')

    def test_call_command_with_tsv_format(self):
        stdout = StringIO()

        call_command('adminsitelog', '--format', 'tsv', stdout=stdout)

        rows = list(csv.reader(StringIO(stdout.getvalue()), delimiter='\t'))
        self.assertEqual(
            rows[0],
            ['id', 'action', 'detail', 'user', 'time'])
        self.assertEqual(rows[1][0], str(self.log.id))
        self.assertEqual(rows[1][1], 'Added')
        self.assertEqual(rows[1][2], 'Item, with comma')
        self.assertEqual(rows[1][3], 'admin')

    def test_call_command_with_csv_format_and_delete_keeps_stdout_parseable(self):
        stdout = StringIO()
        stderr = StringIO()

        call_command(
            'adminsitelog', '--format', 'csv', '--delete', '-y',
            stdout=stdout, stderr=stderr)

        rows = list(csv.reader(StringIO(stdout.getvalue())))
        self.assertEqual(len(rows), 2)
        self.assertIn('delete complete', stderr.getvalue())
        self.assertEqual(LogEntry.objects.count(), 0)

    def test_text_format_delete_writes_report_to_stderr(self):
        stdout = StringIO()
        stderr = StringIO()

        call_command(
            'adminsitelog', '--delete', '-y',
            stdout=stdout, stderr=stderr)

        self.assertIn('delete complete', stderr.getvalue())
        self.assertNotIn('delete complete', stdout.getvalue())
        self.assertEqual(LogEntry.objects.count(), 0)

    def test_unsupported_format_raises_command_error(self):
        with self.assertRaises(CommandError):
            call_command('adminsitelog', format='xml')
