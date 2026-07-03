import csv
from io import StringIO
from types import SimpleNamespace
from unittest import mock

from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.core.management.base import CommandError

from django_boost.contrib.admin_tools.management.commands.adminsitelog import (
    Command,
)
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

    def test_get_log_entry_model_without_admin_raises_command_error(self):
        command = Command()
        with mock.patch('django.apps.apps.is_installed', return_value=False):
            with self.assertRaises(CommandError):
                command.get_log_entry_model()

    def test_sortable_fields_help_without_admin_returns_fallback(self):
        command = Command()
        with mock.patch('django.apps.apps.is_installed', return_value=False):
            self.assertIn(
                'django.contrib.admin', command.get_sortable_fields_help())

    def test_filter_and_exclude_narrow_logs(self):
        changed = LogEntry.objects.create(
            user=self.user, content_type=self.content_type, object_id='2',
            object_repr='Other', action_flag=CHANGE, change_message='x')
        stdout = StringIO()

        call_command(
            'adminsitelog', '--format', 'csv',
            '--filter', 'action_flag=1', '--exclude', 'object_id=99',
            stdout=stdout)

        ids = [row[0] for row in csv.reader(StringIO(stdout.getvalue()))][1:]
        self.assertIn(str(self.log.id), ids)
        self.assertNotIn(str(changed.id), ids)

    def test_invalid_filter_operator_raises(self):
        with self.assertRaisesRegex(CommandError, 'Unsupported filter operation'):
            call_command(
                'adminsitelog', '--filter', 'nooperatorhere', stdout=StringIO())

    def test_invalid_filter_field_raises_command_error(self):
        with self.assertRaises(CommandError):
            call_command(
                'adminsitelog', '--filter', 'badfield=1', stdout=StringIO())

    def test_invalid_order_by_field_raises_command_error(self):
        with self.assertRaises(CommandError):
            call_command(
                'adminsitelog', '--order_by', 'badfield', stdout=StringIO())

    def test_text_format_styles_changed_and_deleted_actions(self):
        LogEntry.objects.create(
            user=self.user, content_type=self.content_type, object_id='2',
            object_repr='Changed object', action_flag=CHANGE,
            change_message='Changed color.')
        LogEntry.objects.create(
            user=self.user, content_type=self.content_type, object_id='3',
            object_repr='Deleted object', action_flag=DELETION,
            change_message='')
        stdout = StringIO()

        call_command('adminsitelog', '--no-color', stdout=stdout)

        output = stdout.getvalue()
        self.assertIn('Changed', output)
        self.assertIn('Deleted', output)

    def test_name_field_option_uses_named_attribute(self):
        stdout = StringIO()

        call_command(
            'adminsitelog', '--format', 'csv', '--name_field', 'email',
            stdout=stdout)

        rows = list(csv.reader(StringIO(stdout.getvalue())))
        self.assertEqual(rows[1][3], 'admin@example.com')

    def test_unknown_name_field_raises_command_error(self):
        with self.assertRaises(CommandError):
            call_command(
                'adminsitelog', '--name_field', 'nope', stdout=StringIO())

    def test_user_name_fallback_uses_email_without_username(self):
        user = SimpleNamespace(email='audit@example.com')
        self.assertEqual(
            Command()._get_user_name(user), 'audit@example.com')

    def test_reports_when_no_logs(self):
        LogEntry.objects.all().delete()
        stderr = StringIO()

        call_command('adminsitelog', stderr=stderr)

        self.assertIn('No logs', stderr.getvalue())

    def test_delete_cancelled_keeps_logs(self):
        stderr = StringIO()

        with mock.patch('builtins.input', return_value='n'):
            call_command(
                'adminsitelog', '--delete', stdout=StringIO(), stderr=stderr)

        self.assertIn('operation canceled', stderr.getvalue())
        self.assertEqual(LogEntry.objects.count(), 1)

    def test_delete_confirmed_via_prompt_deletes_logs(self):
        stderr = StringIO()

        with mock.patch('builtins.input', return_value='y'):
            call_command(
                'adminsitelog', '--delete', stdout=StringIO(), stderr=stderr)

        self.assertIn('delete complete', stderr.getvalue())
        self.assertEqual(LogEntry.objects.count(), 0)

    def _ids_with_filter(self, expr):
        stdout = StringIO()
        call_command(
            'adminsitelog', '--format', 'csv', '--filter', expr, stdout=stdout)
        return [row[0] for row in csv.reader(StringIO(stdout.getvalue()))][1:]

    def test_filter_comparison_operators(self):
        changed = LogEntry.objects.create(
            user=self.user, content_type=self.content_type, object_id='2',
            object_repr='Changed', action_flag=CHANGE, change_message='x')
        deleted = LogEntry.objects.create(
            user=self.user, content_type=self.content_type, object_id='3',
            object_repr='Deleted', action_flag=DELETION, change_message='')

        self.assertEqual(
            set(self._ids_with_filter('action_flag>=2')),
            {str(changed.id), str(deleted.id)})
        self.assertEqual(
            self._ids_with_filter('action_flag<2'), [str(self.log.id)])
        self.assertEqual(
            self._ids_with_filter('action_flag>2'), [str(deleted.id)])
        self.assertEqual(
            self._ids_with_filter('action_flag<=1'), [str(self.log.id)])

    def test_parse_filter_splits_on_leftmost_operator(self):
        # A '>=' inside the value must not be picked over the leading '='; the
        # leftmost operator is the field/value boundary.
        self.assertEqual(
            Command()._parse_filter('object_repr=val>=x'),
            {'object_repr__exact': 'val>=x'})

    def test_parse_filter_comparison_operators(self):
        command = Command()
        self.assertEqual(command._parse_filter('n>=5'), {'n__gte': '5'})
        self.assertEqual(command._parse_filter('n<=5'), {'n__lte': '5'})
        self.assertEqual(command._parse_filter('n>5'), {'n__gt': '5'})
        self.assertEqual(command._parse_filter('n<5'), {'n__lt': '5'})
        self.assertEqual(command._parse_filter('n=5'), {'n__exact': '5'})

    def test_order_by_orders_output(self):
        second = LogEntry.objects.create(
            user=self.user, content_type=self.content_type, object_id='2',
            object_repr='Second', action_flag=CHANGE, change_message='x')
        stdout = StringIO()

        call_command(
            'adminsitelog', format='csv', order_by=['-id'], stdout=stdout)

        ids = [row[0] for row in csv.reader(StringIO(stdout.getvalue()))][1:]
        self.assertEqual(ids, [str(second.id), str(self.log.id)])
