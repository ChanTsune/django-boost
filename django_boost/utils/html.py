from __future__ import annotations

from html import escape
from html.parser import HTMLParser
from io import StringIO


class HTMLSpaceLessCompressor(HTMLParser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buffer = StringIO()
        self.pre_count = 0

    def handle_data(self, data):
        if self.pre_count == 0:
            data = data.strip()
        # convert_charrefs already decoded entities here; re-escape them.
        self.buffer.write(escape(data, quote=False))

    def handle_starttag(self, tag, attrs):
        self.buffer.write("<%s" % tag)
        if attrs:
            self.buffer.write(' ')
            self.buffer.write(self._render_attrs(attrs))
        self.buffer.write('>')
        if tag == 'pre':
            self.pre_count += 1

    def handle_endtag(self, tag):
        self.buffer.write("</%s>" % tag)
        if tag == 'pre':
            self.pre_count -= 1

    def handle_startendtag(self, tag, attrs):
        self.buffer.write("<%s" % tag)
        if attrs:
            self.buffer.write(' ')
            self.buffer.write(self._render_attrs(attrs))
        self.buffer.write("/>")

    def handle_decl(self, data):
        self.buffer.write("<!%s>" % data)

    def _render_attrs(self, attrs):
        return ' '.join('%s="%s"' % attr for attr in attrs)

    def compress(self, data):
        self.feed(data)
        self.reset()
        return self.buffer.getvalue()


def strip_spaces_between_tags(value):
    value = HTMLSpaceLessCompressor().compress(value)
    return value
