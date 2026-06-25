from django_boost.test import TestCase
from django_boost.utils.html import strip_spaces_between_tags


class SpaceLessEntityEscapingTests(TestCase):
    """Compression must not undo HTML escaping in text content."""

    def test_named_entity_in_text_is_preserved(self):
        self.assertEqual(
            strip_spaces_between_tags('<p>a &amp; b</p>'),
            '<p>a &amp; b</p>')

    def test_escaped_markup_is_not_decoded_into_active_markup(self):
        self.assertEqual(
            strip_spaces_between_tags('<p>&lt;script&gt;</p>'),
            '<p>&lt;script&gt;</p>')


class SpaceLessAttributeRenderingTests(TestCase):
    """Attributes must round-trip without inventing values or breaking quotes."""

    def test_valueless_attribute_renders_without_a_value(self):
        self.assertEqual(
            strip_spaces_between_tags('<input disabled>'),
            '<input disabled>')

    def test_attribute_value_is_escaped(self):
        self.assertEqual(
            strip_spaces_between_tags('<a title="x&quot;y">z</a>'),
            '<a title="x&quot;y">z</a>')


class SpaceLessTrailingDataTests(TestCase):
    """Text the parser buffers at end-of-input must not be silently dropped."""

    def test_trailing_text_ending_in_an_ampersand_is_kept(self):
        # A trailing "&" looks like the start of an entity, so the parser
        # holds the run until close(); without close() it is dropped.
        self.assertEqual(
            strip_spaces_between_tags('<p>x</p>price is 5 USD &'),
            '<p>x</p>price is 5 USD &amp;')
