from __future__ import annotations

from html import escape
from html.parser import HTMLParser
from io import StringIO
from typing import Any


class HTMLSpaceLessCompressor(HTMLParser):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.buffer = StringIO()
        self.pre_count = 0

    def handle_data(self, data: str) -> None:
        if self.pre_count == 0:
            data = data.strip()
        # convert_charrefs already decoded entities here; re-escape them.
        self.buffer.write(escape(data, quote=False))

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.buffer.write("<%s" % tag)
        if attrs:
            self.buffer.write(' ')
            self.buffer.write(self._render_attrs(attrs))
        self.buffer.write('>')
        if tag == 'pre':
            self.pre_count += 1

    def handle_endtag(self, tag: str) -> None:
        self.buffer.write("</%s>" % tag)
        if tag == 'pre':
            self.pre_count -= 1

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.buffer.write("<%s" % tag)
        if attrs:
            self.buffer.write(' ')
            self.buffer.write(self._render_attrs(attrs))
        self.buffer.write("/>")

    def handle_decl(self, decl: str) -> None:
        self.buffer.write("<!%s>" % decl)

    def _render_attrs(self, attrs: list[tuple[str, str | None]]) -> str:
        return ' '.join(
            name if value is None else '%s="%s"' % (name, escape(value))
            for name, value in attrs)

    def compress(self, data: str) -> str:
        self.feed(data)
        # close() flushes trailing buffered text; reset() would drop it.
        self.close()
        return self.buffer.getvalue()


def strip_spaces_between_tags(value: str) -> str:
    value = HTMLSpaceLessCompressor().compress(value)
    return value
