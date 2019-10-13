from django_boost.test import TestCase
from django_boost.urls import UrlSet


class TestUrlSet(TestCase):

    def test_urlset(self):
        class SampleUrlSet(UrlSet):
            app_name = 'sample'
            urlpatterns = []
        self.assertFalse(hasattr(UrlSet, 'urlpatterns'))
        self.assertFalse(hasattr(UrlSet, 'app_name'))

        self.assertTrue(hasattr(SampleUrlSet, 'urlpatterns'))
        self.assertTrue(hasattr(SampleUrlSet, 'app_name'))
