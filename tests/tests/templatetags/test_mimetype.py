from django_boost.test import TestCase


class TestMimetypeTemplateTag(TestCase):

    def test_mimetype(self):
        from mimetypes import guess_type
        from django_boost.templatetags.mimetype import mimetype

        application_json = guess_type('a.json')[0]
        case = [
            (application_json, 'json'),
            (application_json, '.json'),
            (application_json, 'a.json'),
        ]
        for t, c in case:
            self.assertEqual(t, mimetype(c))

    def test_mimetype_unknown_extension_returns_empty_string(self):
        from django_boost.templatetags.mimetype import mimetype
        self.assertEqual(mimetype('file.unknownext'), '')
        self.assertEqual(mimetype('unknownext'), '')

    def test_mimetype_coerces_non_string_input(self):
        # str(123) == '123' happens to match a registered extension, so
        # only the return type (not a specific value) is asserted here.
        from django_boost.templatetags.mimetype import mimetype
        self.assertEqual(mimetype(None), '')
        self.assertIsInstance(mimetype(123), str)
