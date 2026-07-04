from django.test.client import RequestFactory

from django_boost.test import TestCase


class UrlencodeFilterTests(TestCase):

    def test_urlencode(self):
        from django_boost.templatetags.boost_url import urlencode
        cases = [
            ("日本語", "%E6%97%A5%E6%9C%AC%E8%AA%9E"),
            ("https://google.com", "https%3A//google.com")
        ]
        for a, e in cases:
            self.assertEqual(urlencode(a), e)

    def test_urlencode_coerces_non_string_input(self):
        # Like Django's built-in urlencode filter, coerce to str instead of
        # raising TypeError on a non-string value (e.g. an int or None).
        from django_boost.templatetags.boost_url import urlencode
        self.assertEqual(urlencode(123), "123")
        self.assertEqual(urlencode(None), "None")


class UrldecodeFilterTests(TestCase):

    def test_urldecode(self):
        from django_boost.templatetags.boost_url import urldecode

        cases = [
            ("%E6%97%A5%E6%9C%AC%E8%AA%9E", "日本語"),
            ("https%3A//google.com", "https://google.com")
        ]
        for a, e in cases:
            self.assertEqual(urldecode(a), e)

    def test_urldecode_coerces_non_string_input(self):
        from django_boost.templatetags.boost_url import urldecode
        self.assertEqual(urldecode(123), "123")
        self.assertEqual(urldecode(None), "None")

    def test_urldecode_output_is_escaped_in_autoescaped_template(self):
        from django.template import Context, Template
        from django.utils.safestring import mark_safe

        template = Template("{% load boost_url %}{{ value|urldecode }}")
        output = template.render(Context({"value": mark_safe("%3Cscript%3E")}))
        self.assertEqual(output, "&lt;script&gt;")

    def test_urldecode_output_is_raw_when_autoescape_off(self):
        from django.template import Context, Template
        from django.utils.safestring import mark_safe

        template = Template(
            "{% load boost_url %}"
            "{% autoescape off %}{{ value|urldecode }}{% endautoescape %}"
        )
        output = template.render(Context({"value": mark_safe("%3Cscript%3E")}))
        self.assertEqual(output, "<script>")


class ReplaceParametersTagTests(TestCase):

    def test_replace_parameters(self):
        from django_boost.templatetags.boost_url import replace_parameters

        cases = [
            ("", ('p', 'p'), ("p=p",)),
            ("q=q", ('p', 'p'), ("q=q", "p=p")),
            ("q=q", ('q', 'x', 'p', 'p'), ("q=x", "p=p")),
        ]
        factory = RequestFactory()
        for qs, args, expected in cases:
            request = factory.request(**{'QUERY_STRING': qs})
            actual = replace_parameters(request, *args)
            for e in expected:
                self.assertIn(e, actual)

        with self.assertRaisesRegex(LookupError, "must be even"):
            request = factory.request()
            replace_parameters(request, 'q')


class GetQuerystringTagTests(TestCase):

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
