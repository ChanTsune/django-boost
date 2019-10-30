Custom User
=========================

:synopsis: django-boost custom user


EmailUser
----------

Configuration
^^^^^^^^^^^^^

Setting of your Django project *settings.py* file.

::

  AUTH_USER_MODEL = 'django_boost.EmailUser'


Replace Django default user model.

Use email address instead of username when logging in.


AbstractEmailUser
-----------------

Available when you want to add a field to ``EmailUser``.

Inherit ``AbstractEmailUser`` and add fields.

example::

  from django.db import models
  from django_boost.models import AbstractEmailUser

  class CustomUser(AbstractEmailUser):
      is_flozen = models.BoolField(default=False)
      homepage = models.URLField()
