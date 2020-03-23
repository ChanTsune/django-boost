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
        self.buffer.write(data)

    def handle_starttag(self, tag, attrs):
        self.buffer.write("<%s>" % tag)
        if tag == 'pre':
            self.pre_count += 1

    def handle_endtag(self, tag):
        self.buffer.write("</%s>" % tag)
        if tag == 'pre':
            self.pre_count -= 1

    def handle_startendtag(self, tag, attrs):
        self.buffer.write("<%s/>" % tag)

    def handle_decl(self, data):
        self.buffer.write("<!%s>" % data)

    def compress(self, data):
        self.feed(data)
        return self.buffer.getvalue()
