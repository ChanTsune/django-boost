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


class TestStaticFileBelow(TestCase):

    def test_connect(self):
        import os
        from django.urls import URLPattern
        from django_boost.urls.static import load_static_files

        ROOT_DIR = os.path.dirname(__file__)

        urlpatterns = load_static_files(ROOT_DIR)

        for p in urlpatterns:
            self.assertTrue(isinstance(p, URLPattern))

    def test_angle_bracket_filename_routes_literally(self):
        import os
        import shutil
        import tempfile
        from django_boost.urls.static import load_static_files

        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp)
        with open(os.path.join(tmp, '<script>.js'), 'w') as f:
            f.write('x')

        (pattern,) = [p.pattern for p in load_static_files(tmp)]
        # The file name must match itself literally, not act as a path
        # converter that captures any "<something>.js".
        self.assertIsNotNone(pattern.match('<script>.js'))
        self.assertIsNone(pattern.match('anything.js'))
