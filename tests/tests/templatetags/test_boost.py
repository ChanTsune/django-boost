from django_boost.test import TestCase


class TestBoostTemplateTag(TestCase):

    def test_abs(self):
        from django_boost.templatetags.boost import _abs

        self.assertEqual(_abs(1), 1)
        self.assertEqual(_abs(-1), 1)
        self.assertEqual(_abs(0), 0)

    def test_all(self):
        from django_boost.templatetags.boost import _all

        self.assertTrue(_all([True]))
        self.assertFalse(_all([False, False]))
        self.assertFalse(_all([False]))

    def test_any(self):
        from django_boost.templatetags.boost import _any

        self.assertFalse(_any([False]))
        self.assertTrue(_any([True]))
        self.assertTrue(_any([True, False]))

    def test_ascii(self):
        from django_boost.templatetags.boost import _ascii

        self.assertEqual(_ascii(1), '1')

    def test_bin(self):
        from django_boost.templatetags.boost import _bin

        self.assertEqual(_bin(1), "0b1")

    def test_bool(self):
        from django_boost.templatetags.boost import _bool

        self.assertEqual(_bool(1), True)

    def test_next_filter(self):
        from django_boost.templatetags.boost import _next

        iterator = iter([10, 20, 30])

        self.assertEqual(_next(iterator), 10)
        self.assertEqual(_next(iterator), 20)

    def test_zip_filter(self):
        import warnings

        from django_boost.templatetags.boost import _zip

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = _zip([1, 2], [3, 4])

        self.assertEqual(caught, [])
        self.assertEqual(list(result), [(1, 3), (2, 4)])
