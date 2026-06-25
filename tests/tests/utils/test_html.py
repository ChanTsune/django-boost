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
