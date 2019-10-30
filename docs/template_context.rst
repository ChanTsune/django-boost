Template context
=========================

:synopsis: context processor in django-boost

User Agent
-----------

Configuration
^^^^^^^^^^^^^

::

  TEMPLATES = [
      {
          'BACKEND': 'django.template.backends.django.DjangoTemplates',
          'DIRS': [],
          'APP_DIRS': True,
          'OPTIONS': {
              'context_processors': [
                  'django.template.context_processors.debug',
                  'django.template.context_processors.request',
                  'django.contrib.auth.context_processors.auth',
                  'django.contrib.messages.context_processors.messages',
                  'django_boost.context_processors.user_agent', # add
              ],
          },
      },
  ]

When given a user agent like ``Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36``, provide the following context to the template.

::

  {'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
  'browser': 'Chrome',
  'device': 'Other',
  'is_bot': False,
  'is_email_client': False,
  'is_mobile': False,
  'is_pc': True,
  'is_tablet': False,
  'is_touch_capable': False,
  'os': 'Mac OS X'}

These information is obtained using `user-agents <https://github.com/selwin/python-user-agents>`_
