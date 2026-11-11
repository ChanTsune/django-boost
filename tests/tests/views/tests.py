import os

from django.test import override_settings
from django.urls import reverse
from django_boost.test import TestCase
from django_boost.views.base import StaticView

ROOT_PATH = os.path.dirname(__file__)


@override_settings(
    ROOT_URLCONF='tests.tests.views.urls',
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(ROOT_PATH, 'templates')],
        'APP_DIRS': True,
    }],
)
class TestStringView(TestCase):

    def test_string_view(self):
        response = self.client.get(reverse('empty'))
        self.assertEqual(response.content, b'')

    def test_string_view_content(self):
        response = self.client.get(reverse('simple'))
        self.assertEqual(response.content, b'test string')

    def test_string_view_get_content(self):
        cases = [
            {'key1': 1, 'key2': 'one'}
        ]
        for e in cases:
            response = self.client.get(reverse('dynamic', kwargs=e))
            self.assertEqual(response.content, str(e).encode('utf-8'))


class RemovedLegacyViewsTests(TestCase):
    def test_legacy_classes_are_not_available(self):
        import django_boost.views.base as base
        import django_boost.views.generic as generic

        legacy_names = (
            "View", "TemplateView", "FormView", "CreateView",
            "ListView", "DetailView", "UpdateView", "DeleteView",
        )
        for module in (base, generic):
            for name in legacy_names:
                with self.subTest(module=module.__name__, name=name):
                    self.assertFalse(hasattr(module, name))

    def test_supported_views_remain_available(self):
        from django_boost.views.generic import JsonView, ModelCRUDViews, StaticView
        self.assertTrue(all((JsonView, ModelCRUDViews, StaticView)))


class StaticViewContentTypeTests(TestCase):
    """StaticView with an explicit content_type must serve, not crash."""

    def test_explicit_content_type_does_not_crash(self):
        class FileView(StaticView):
            static_name = os.path.abspath(__file__)
            content_type = 'text/plain'

        response = FileView().create_response()
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'text/plain')
        finally:
            response.close()

    def test_guessed_content_type_still_works(self):
        class FileView(StaticView):
            static_name = os.path.abspath(__file__)

        response = FileView().create_response()
        try:
            self.assertEqual(response.status_code, 200)
        finally:
            response.close()


class StaticViewMissingFileTests(TestCase):
    """A StaticView whose file is gone responds 404, not 500."""

    def test_missing_file_raises_http404(self):
        from django.http import Http404
        from django.test import RequestFactory

        class FileView(StaticView):
            static_name = os.path.join(
                os.path.dirname(__file__), 'does_not_exist.xyz')

        with self.assertRaises(Http404):
            FileView().get(RequestFactory().get('/missing'))
