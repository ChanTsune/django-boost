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
