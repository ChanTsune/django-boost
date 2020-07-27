from django.test.client import RequestFactory

from django_boost.test import TestCase


class TestBoostTemplateTag(TestCase):
    pass


class TestBoostUrlTemplateTag(TestCase):
    
    def test_urlencode(self):
        from django_boost.templatetags.boost_url import urlencode
        cases = [
            ("日本語", "%E6%97%A5%E6%9C%AC%E8%AA%9E"),
            ("https://google.com", "https%3A//google.com")
        ]
        for a, e in cases:
            self.assertEqual(urlencode(a), e)

    def test_urldecode(self):
        from django_boost.templatetags.boost_url import urldecode

        cases = [
            ("%E6%97%A5%E6%9C%AC%E8%AA%9E", "日本語"),
            ("https%3A//google.com", "https://google.com")
        ]
        for a, e in cases:
            self.assertEqual(urldecode(a), e)

    def test_replace_parameters(self):
        from django_boost.templatetags.boost_url import replace_parameters

        cases = [
            ("", ('p', 'p'), "p=p"),
            ("q=q", ('p', 'p'), "q=q&p=p"),
            ("q=q", ('q', 'x', 'p', 'p'), "q=x&p=p"),
        ]
        factory = RequestFactory()
        for qs, args, expected in cases:
            request = factory.request(**{'QUERY_STRING': qs})
            self.assertEqual(replace_parameters(request, *args), expected)
        
        with self.assertRaises(LookupError):
            request = factory.request()
            replace_parameters(request, 'q')

    def test_get_querystring(self):
        from django_boost.templatetags.boost_url import get_querystring

        cases = [
            ("", "q", None),
            ("q=q", "q", "q"),
            ("q=q&q=j&q=k", "q", "k"),
        ]
        factory = RequestFactory()
        for qs, key, value in cases:
            request = factory.request(**{'QUERY_STRING': qs})
            self.assertEqual(get_querystring(request, key), value)



class TestBoostQueryTemplateTag(TestCase):
    pass


class TestMimeTypeTempleteTag(TestCase):

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
