from django.utils.deprecation import MiddlewareMixin
from django_boost.utils.html import strip_spaces_between_tags


class SpaceLessMiddleware(MiddlewareMixin):
    """
    Middleware that remove white space in HTML.

    You will need to add the *SpaceLessMiddleware* to the MIDDLEWARE
    setting of your Django project *settings.py* file.

    ::

      MIDDLEWARE = [
          'django_boost.middleware.SpaceLessMiddleware',  # add
          'django.middleware.security.SecurityMiddleware',
          'django.contrib.sessions.middleware.SessionMiddleware',
          ...
      ]


    Install so that it is executed before middleware
    to compress such as GZipMiddleware.

    """

    def __call__(self, request):
        response = self.get_response(request)
        if 'text/html' in response.get('Content-Type', ''):
            if response.streaming:
                response.streaming_content = strip_spaces_between_tags(
                    response.streaming_content.decode())
            else:
                response.content = strip_spaces_between_tags(
                    response.content.decode())
                response['Content-Length'] = str(len(response.content))
        return response
