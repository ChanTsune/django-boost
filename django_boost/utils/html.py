"""HTML whitespace-compression helpers."""

from __future__ import annotations

import codecs
from collections.abc import AsyncIterable, AsyncIterator, Iterable, Iterator
from html import escape
from html.parser import HTMLParser
from io import StringIO
from typing import Any


class HTMLSpaceLessCompressor(HTMLParser):
    """Streaming HTML parser that removes ignorable whitespace between tags."""

    RAW_TEXT_ELEMENTS = frozenset({'script', 'style'})
    WHITESPACE_PRESERVING_ELEMENTS = frozenset({'pre', 'textarea'})

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the output buffer and whitespace-tracking state."""
        super().__init__(*args, **kwargs)
        self.buffer = StringIO()
        self._raw_depth = 0
        self._preserve_depth = 0
        self._run_started = False
        self._pending_ws = ''

    def _end_run(self) -> None:
        # End of a text run (tag boundary or close()): drop the trailing
        # whitespace held back below (rstrip) and reset for the next run.
        self._pending_ws = ''
        self._run_started = False

    def handle_data(self, data: str) -> None:
        if self._raw_depth > 0:
            # Raw CDATA (script/style): escaping would corrupt the JS/CSS.
            self.buffer.write(data)
            return
        if self._preserve_depth > 0:
            # pre/textarea: whitespace is significant, so re-escape but keep it.
            self.buffer.write(escape(data, quote=False))
            return
        # Default: strip the run as a whole but stream its interior as it
        # arrives — drop leading whitespace, then hold back only trailing
        # whitespace until the run continues (more data) or ends (a tag).
        # convert_charrefs decoded entities, so re-escape.
        if not self._run_started:
            data = data.lstrip()
            if not data:
                return
            self._run_started = True
        else:
            data = self._pending_ws + data
        stripped = data.rstrip()
        self._pending_ws = data[len(stripped):]
        self.buffer.write(escape(stripped, quote=False))

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._end_run()
        self.buffer.write("<%s" % tag)
        if attrs:
            self.buffer.write(' ')
            self.buffer.write(self._render_attrs(attrs))
        self.buffer.write('>')
        if tag in self.RAW_TEXT_ELEMENTS:
            self._raw_depth += 1
        elif tag in self.WHITESPACE_PRESERVING_ELEMENTS:
            self._preserve_depth += 1

    def handle_endtag(self, tag: str) -> None:
        self._end_run()
        self.buffer.write("</%s>" % tag)
        if tag in self.RAW_TEXT_ELEMENTS:
            self._raw_depth -= 1
        elif tag in self.WHITESPACE_PRESERVING_ELEMENTS:
            self._preserve_depth -= 1

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._end_run()
        self.buffer.write("<%s" % tag)
        if attrs:
            self.buffer.write(' ')
            self.buffer.write(self._render_attrs(attrs))
        self.buffer.write("/>")

    def handle_decl(self, decl: str) -> None:
        self._end_run()
        self.buffer.write("<!%s>" % decl)

    def handle_comment(self, data: str) -> None:
        # Comments are dropped, but a comment still ends the current text run
        # so the text on either side is stripped separately, as with a tag.
        self._end_run()

    def _render_attrs(self, attrs: list[tuple[str, str | None]]) -> str:
        return ' '.join(
            name if value is None else '%s="%s"' % (name, escape(value))
            for name, value in attrs)

    def close(self) -> None:
        # super().close() flushes text the parser was still buffering (e.g. a
        # trailing "&" that looked like the start of an entity); _end_run()
        # then drops that last run's trailing whitespace.
        super().close()
        self._end_run()

    def _drain(self) -> str:
        out = self.buffer.getvalue()
        self.buffer = StringIO()
        return out

    def feed_chunk(self, data: str) -> str:
        """Feed one chunk and return the compressed output produced so far.

        Only undecided trailing state stays buffered until finalize(): the
        run's trailing whitespace (held back for rstrip), and any input
        HTMLParser cannot resolve yet (a dangling "&" or a partial tag).
        """
        self.feed(data)
        return self._drain()

    def finalize(self) -> str:
        """Emit text buffered after the last tag and close the parser.

        Call once, last; the compressor is single-use afterward.
        """
        self.close()
        return self._drain()

    def compress(self, data: str) -> str:
        return self.feed_chunk(data) + self.finalize()


def strip_spaces_between_tags(value: str) -> str:
    """Remove ignorable whitespace between HTML tags in a single, already-complete string."""
    return HTMLSpaceLessCompressor().compress(value)


def compress_stream(chunks: Iterable[bytes], charset: str) -> Iterator[bytes]:
    """Remove ignorable whitespace between HTML tags across a chunked byte stream."""
    compressor = HTMLSpaceLessCompressor()
    decoder = codecs.getincrementaldecoder(charset)()
    for chunk in chunks:
        out = compressor.feed_chunk(decoder.decode(chunk))
        if out:
            yield out.encode(charset)
    # Flush the decoder (final=True surfaces a truncated trailing multibyte),
    # then finalize() emits the parser's last buffered text.
    out = compressor.feed_chunk(decoder.decode(b'', final=True)) + compressor.finalize()
    if out:
        yield out.encode(charset)


async def acompress_stream(chunks: AsyncIterable[bytes], charset: str) -> AsyncIterator[bytes]:
    """Async counterpart to ``compress_stream``, for an async byte-chunk source."""
    compressor = HTMLSpaceLessCompressor()
    decoder = codecs.getincrementaldecoder(charset)()
    async for chunk in chunks:
        out = compressor.feed_chunk(decoder.decode(chunk))
        if out:
            yield out.encode(charset)
    # Final decode flush + finalize; see compress_stream for the rationale.
    out = compressor.feed_chunk(decoder.decode(b'', final=True)) + compressor.finalize()
    if out:
        yield out.encode(charset)
