from django.utils.deprecation import MiddlewareMixin
from django_boost.utils.html import strip_spaces_between_tags


class SpaceLessMiddleWare(MiddlewareMixin):

    def __call__(self, request):
        response = self.get_response(request)
        if 'text/html' in response.get('Content-Type', ''):
            response.content = strip_spaces_between_tags(response.content.decode())
        return response
