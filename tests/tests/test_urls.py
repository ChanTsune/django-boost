from django_boost.test import TestCase


class TestUrlSet(TestCase):

    def test_urlset(self):
        from django_boost.urls import UrlSet

        class SampleUrlSet(UrlSet):
            app_name = 'sample'
            urlpatterns = []
        self.assertFalse(hasattr(UrlSet, 'urlpatterns'))
        self.assertFalse(hasattr(UrlSet, 'app_name'))

        self.assertTrue(hasattr(SampleUrlSet, 'urlpatterns'))
        self.assertTrue(hasattr(SampleUrlSet, 'app_name'))


class TestStaticFileBerow(TestCase):

    def test_connect(self):
        import os
        from django.urls import URLPattern
        from django_boost.urls.static import load_static_files

        ROOT_DIR = os.path.dirname(__file__)

        urlpatterns = load_static_files(ROOT_DIR)

        for p in urlpatterns:
            self.assertTrue(isinstance(p, URLPattern))
