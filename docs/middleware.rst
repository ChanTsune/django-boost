Middlewares
=========================

:synopsis: Middlewares in django-boost



RedirectCorrectHostnameMiddleware
-----------------------------------

Configuration
^^^^^^^^^^^^^

You will need to add the *RedirectCorrectHostnameMiddleware* to the MIDDLEWARE
setting of your Django project *settings.py* file.

::

  MIDDLEWARE = [
      'django_boost.middleware.RedirectCorrectHostnameMiddleware',  # add
      'django.middleware.security.SecurityMiddleware',
      'django.contrib.sessions.middleware.SessionMiddleware',
      ...
  ]

  CORRECT_HOST = 'sample.com'


Redirect all access to the domain specified in ``CORRECT_HOST``

It is not redirected when ``DEBUG = True``

This is useful when migrating domains

Originally it should be done with server software such as nginx and apache, but it is useful when the setting is troublesome or when using services such as heroku


HttpStatusCodeExceptionMiddleware
----------------------------------

You will need to add the *HttpStatusCodeExceptionMiddleware* to the MIDDLEWARE
setting of your Django project *settings.py* file.

::

  MIDDLEWARE = [
      'django_boost.middleware.HttpStatusCodeExceptionMiddleware',  # add
      'django.middleware.security.SecurityMiddleware',
      'django.contrib.sessions.middleware.SessionMiddleware',
      ...
  ]

This Middleware is required when using the :doc:`http_status_code_exceptions`.
