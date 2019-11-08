from django_boost.test import TestCase


class TestBoostTemplateTag(TestCase):
    pass


class TestBoostUrlTemplateTag(TestCase):
    pass


class TestBoostQueryTemplateTag(TestCase):
    pass


class TestMimeTypeTempleteTag(TestCase):

    def test_mimetype(self):
        from mimetypes import guess_type
        from django_boost.templatetags.mime_type import mimetype

        application_json = guess_type('a.json')[0]
        case = [
            (application_json, 'json'),
            (application_json, '.json'),
            (application_json, 'a.json'),
        ]
        for t, c in case:
            self.assertEqual(t, mimetype(c))
