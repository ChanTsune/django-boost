import os
import tempfile
from shutil import rmtree
from unittest.mock import patch

from django.core.management import call_command
from django.core.management.templates import TemplateCommand as DjangoTemplateCommand

from django_boost.management.templates import TemplateCommand
from django_boost.test import TestCase


class StartAppPlusTests(TestCase):

    def setUp(self):
        self.target = tempfile.mkdtemp()

    def tearDown(self):
        if os.path.exists(self.target):
            rmtree(self.target)

    def _generate(self, name='sampleapp'):
        call_command('startapp_plus', name, self.target)

    def _read(self, filename):
        with open(os.path.join(self.target, filename)) as fp:
            return fp.read()

    def test_adds_forms_and_urls(self):
        # django-boost specific additions that Django's template does not ship
        self._generate()
        self.assertTrue(os.path.exists(os.path.join(self.target, 'forms.py')))
        self.assertTrue(os.path.exists(os.path.join(self.target, 'urls.py')))

    def test_urls_app_name_is_rendered(self):
        self._generate(name='myapp')
        # quote style may differ if a formatter post-processes the output
        self.assertRegex(self._read('urls.py'), r"""app_name = ['"]myapp['"]""")

    def test_apps_py_follows_django_base(self):
        # base files come straight from Django, so its defaults are inherited
        self._generate()
        self.assertIn('default_auto_field', self._read('apps.py'))

    def test_apps_py_has_no_ready_stub(self):
        self._generate()
        self.assertNotIn('def ready(', self._read('apps.py'))

    def test_views_py_has_no_generic_imports(self):
        self._generate()
        self.assertNotIn('from django.views.generic', self._read('views.py'))


class ComposeTests(TestCase):

    def setUp(self):
        self.base = tempfile.mkdtemp()
        self.overlay = tempfile.mkdtemp()
        self.addCleanup(rmtree, self.base, True)
        self.addCleanup(rmtree, self.overlay, True)

    @staticmethod
    def _write(directory, name, content):
        with open(os.path.join(directory, name), 'w') as fp:
            fp.write(content)

    def _compose(self):
        command = TemplateCommand()
        command.paths_to_remove = []
        composed = command._compose(self.base, self.overlay)
        self.addCleanup(rmtree, composed, True)
        with open(os.path.join(composed, 'urls.py-tpl')) as fp:
            urls = fp.read()
        with open(os.path.join(composed, 'forms.py-tpl')) as fp:
            forms = fp.read()
        return urls, forms

    def test_base_file_wins_over_overlay(self):
        # if Django ships a file of the same name, defer to it
        self._write(self.base, 'urls.py-tpl', 'BASE')
        self._write(self.overlay, 'urls.py-tpl', 'OVERLAY')
        self._write(self.overlay, 'forms.py-tpl', 'EXTRA')
        urls, forms = self._compose()
        self.assertEqual(urls, 'BASE')
        self.assertEqual(forms, 'EXTRA')


class HandleTemplateTests(TestCase):

    def _handle(self, template, subdir):
        command = TemplateCommand()
        with patch.object(DjangoTemplateCommand, 'handle_template', return_value='BASE') as base:
            result = command.handle_template(template, subdir)
        base.assert_called_once_with(template, subdir)
        return result

    def test_user_supplied_template_skips_overlay(self):
        # an explicit --template bypasses the django-boost overlay
        self.assertEqual(self._handle('https://example.com/app.zip', 'app_template'), 'BASE')

    def test_missing_overlay_returns_base(self):
        # a subdir without a django-boost overlay (e.g. project_template) is returned unchanged
        self.assertEqual(self._handle(None, 'project_template'), 'BASE')
