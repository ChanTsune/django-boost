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

    def test_after_view_process(self):
        response = self.client.get(reverse('after'))
        self.assertEqual(response.content, b'processed')
        self.assertEqual(response["X-After-View-Process"], "yes")

    def test_after_view_process_on_short_circuit(self):
        # A mixin ahead of View in the MRO returns a 415 without calling
        # super().dispatch(); after_view_process must still run on it.
        response = self.client.get(reverse('after_short_circuit'))
        self.assertEqual(response.status_code, 415)
        self.assertEqual(response.get("X-After-View-Process"), "yes")

    def test_after_view_process_on_generic_view(self):
        # The hook fires through a generic view's full dispatch/render path.
        response = self.client.get(reverse('after_generic'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get("X-After-View-Process"), "yes")

    def test_after_view_process_on_head(self):
        response = self.client.head(reverse('after'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get("X-After-View-Process"), "yes")


class DeprecatedViewLayerTests(TestCase):

    DEPRECATED_NAMES = [
        "View", "TemplateView", "FormView", "CreateView",
        "ListView", "DetailView", "UpdateView", "DeleteView",
    ]

    def test_base_module_access_warns(self):
        import django_boost.views.base as base
        for name in self.DEPRECATED_NAMES:
            with self.assertWarns(DeprecationWarning):
                getattr(base, name)

    def test_generic_module_access_warns(self):
        import django_boost.views.generic as generic
        for name in self.DEPRECATED_NAMES:
            with self.assertWarns(DeprecationWarning):
                getattr(generic, name)

    def test_kept_views_do_not_warn(self):
        import warnings

        import django_boost.views.generic as generic
        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            generic.JsonView
            generic.StaticView
            generic.ModelCRUDViews


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
