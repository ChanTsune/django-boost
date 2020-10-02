from django_boost.views.simple import StringView


class SimpleStringView(StringView):
    content = b'test string'


class DynamicStringView(StringView):

    def get_content(self, **kwargs):
        return str(kwargs)
