import asyncio

from django_boost.test import TestCase
from django_boost.utils.html import (
    acompress_stream, compress_stream, strip_spaces_between_tags)


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


class SpaceLessCommentBoundaryTests(TestCase):
    """A comment between text must not merge the surrounding runs."""

    def test_whitespace_around_a_comment_is_collapsed(self):
        # The comment is a run boundary like a tag: "a" and "b" are stripped
        # separately, so the whitespace between them collapses.
        self.assertEqual(
            strip_spaces_between_tags('<p>  a  <!-- c -->  b  </p>'),
            '<p>ab</p>')


class SpaceLessStreamLazinessTests(TestCase):
    """A text run must stream as it arrives, not buffer until the next tag."""

    def test_long_text_node_is_emitted_before_the_closing_tag(self):
        def gen():
            yield b'<html><body>'
            yield b'x' * 50
            yield b'</body></html>'

        chunks = list(compress_stream(gen(), 'utf-8'))

        self.assertIn(b'x' * 50, chunks)
        self.assertEqual(b''.join(chunks), b'<html><body>' + b'x' * 50 + b'</body></html>')


class SpaceLessStreamPreTests(TestCase):
    """<pre> whitespace must survive being split across chunk boundaries."""

    def test_pre_block_whitespace_is_preserved_across_chunk_boundaries(self):
        source = '<pre>  line1\n   line2  </pre>'
        data = source.encode('utf-8')
        streamed = b''.join(
            compress_stream([data[i:i + 4] for i in range(0, len(data), 4)],
                            'utf-8')).decode('utf-8')

        self.assertEqual(streamed, strip_spaces_between_tags(source))
        self.assertEqual(streamed, '<pre>  line1\n   line2  </pre>')


class SpaceLessStreamEquivalenceTests(TestCase):
    """Streamed output must equal batch output for any chunk split."""

    def test_streamed_output_equals_batch_for_various_chunk_sizes(self):
        source = ('<html>  <head>  <title> T </title>  </head>  <body>'
                  '  <p> a  b </p>  <pre>  x  y  </pre>  </body>  </html>')
        batch = strip_spaces_between_tags(source)
        data = source.encode('utf-8')
        for size in (1, 2, 3, 5, 7, 16):
            chunks = [data[i:i + size] for i in range(0, len(data), size)]
            streamed = b''.join(compress_stream(chunks, 'utf-8')).decode('utf-8')
            self.assertEqual(streamed, batch, msg='chunk size %d' % size)


class SpaceLessStreamEntityTests(TestCase):
    """An entity straddling a chunk boundary must reassemble, not split or
    double-escape."""

    def test_entity_split_across_chunk_boundary_matches_batch(self):
        source = '<p>a &amp; b &lt; c</p>'
        batch = strip_spaces_between_tags(source)
        data = source.encode('utf-8')
        for size in (1, 2, 3, 4, 5):
            chunks = [data[i:i + size] for i in range(0, len(data), size)]
            streamed = b''.join(compress_stream(chunks, 'utf-8')).decode('utf-8')
            self.assertEqual(streamed, batch, msg='chunk size %d' % size)


class SpaceLessStreamEdgeCaseTests(TestCase):

    def test_empty_stream_yields_nothing(self):
        self.assertEqual(list(compress_stream([], 'utf-8')), [])

    def test_truncated_trailing_multibyte_raises(self):
        # A stream ending mid-character is malformed; fail loudly rather than
        # emit silently corrupted output.
        with self.assertRaises(UnicodeDecodeError):
            list(compress_stream([b'<p>ok', b'\xe3\x81'], 'utf-8'))


class SpaceLessAsyncStreamEdgeCaseTests(TestCase):
    """acompress_stream is a separate implementation; guard its edges too."""

    def test_empty_async_stream_yields_nothing(self):
        async def agen():
            for _ in ():
                yield b''

        async def run():
            return [chunk async for chunk in acompress_stream(agen(), 'utf-8')]

        self.assertEqual(asyncio.run(run()), [])

    def test_async_truncated_trailing_multibyte_raises(self):
        async def agen():
            yield b'<p>ok'
            yield b'\xe3\x81'  # stream ends mid-character

        async def run():
            return [chunk async for chunk in acompress_stream(agen(), 'utf-8')]

        with self.assertRaises(UnicodeDecodeError):
            asyncio.run(run())


class SpaceLessRawTextElementTests(TestCase):
    """<script>/<style> content is raw (must not be escaped); <textarea>
    whitespace is significant (must not be stripped)."""

    def test_script_content_is_not_escaped(self):
        self.assertEqual(
            strip_spaces_between_tags(
                '<script>if (a < b && c > d) { x = 1; }</script>'),
            '<script>if (a < b && c > d) { x = 1; }</script>')

    def test_style_content_is_not_escaped(self):
        self.assertEqual(
            strip_spaces_between_tags('<style>body > p { color: red; }</style>'),
            '<style>body > p { color: red; }</style>')

    def test_textarea_whitespace_is_preserved(self):
        self.assertEqual(
            strip_spaces_between_tags('<textarea>  a  b  </textarea>'),
            '<textarea>  a  b  </textarea>')


class SpaceLessCDataAndProcessingInstructionTests(TestCase):
    """CDATA sections (valid in inline SVG/MathML) and processing
    instructions must be preserved, not silently dropped."""

    def test_cdata_section_is_preserved(self):
        self.assertEqual(
            strip_spaces_between_tags('<svg><text><![CDATA[a<b]]></text></svg>'),
            '<svg><text><![CDATA[a<b]]></text></svg>')

    def test_processing_instruction_is_preserved(self):
        self.assertEqual(
            strip_spaces_between_tags('a<?instruction?>b'),
            'a<?instruction?>b')


class SpaceLessStreamRawTextTests(TestCase):
    """script/style/textarea must stream identically to batch for any split."""

    SOURCE = ('<html>  <head>  <style> body > p { x: 1 } </style>'
              '  <script>if (a < b) { y(); }</script>  </head>'
              '  <body>  <textarea>  a  b  </textarea>  </body>  </html>')

    def test_sync_streamed_raw_text_equals_batch(self):
        batch = strip_spaces_between_tags(self.SOURCE)
        data = self.SOURCE.encode('utf-8')
        for size in (1, 2, 3, 5, 7, 16):
            chunks = [data[i:i + size] for i in range(0, len(data), size)]
            streamed = b''.join(compress_stream(chunks, 'utf-8')).decode('utf-8')
            self.assertEqual(streamed, batch, msg='chunk size %d' % size)

    def test_async_streamed_raw_text_equals_batch(self):
        batch = strip_spaces_between_tags(self.SOURCE)
        data = self.SOURCE.encode('utf-8')

        async def run(size):
            chunks = [data[i:i + size] for i in range(0, len(data), size)]

            async def agen():
                for chunk in chunks:
                    yield chunk

            return b''.join(
                [p async for p in acompress_stream(agen(), 'utf-8')]).decode('utf-8')

        for size in (1, 3, 7):
            self.assertEqual(asyncio.run(run(size)), batch, msg='chunk size %d' % size)
