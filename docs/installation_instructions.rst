Installation instructions
=========================

:synopsis: Installing django-boost

Installation
------------

For usage
^^^^^^^^^

You can use pip to install django-boost for usage::

  $ pip install django-boost

For development
^^^^^^^^^^^^^^^

django-boost is hosted on github::

 https://github.com/ChanTsune/django-boost

Source code can be accessed by performing a Git clone.


Configuration
^^^^^^^^^^^^^

You will need to add the *django_boost* application to the INSTALLED_APPS
setting of your Django project *settings.py* file.::

  INSTALLED_APPS = [
      ...
      'django_boost',
  ]

This will make sure that Django finds the additional management commands
provided by *django-boost*.

The next time you invoke *./manage.py help* you should be able to see all the
newly available commands.
