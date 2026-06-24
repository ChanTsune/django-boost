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
setting of your Django project *settings.py* file.

::

  INSTALLED_APPS = [
      ...
      'django_boost',
  ]

This will make sure that Django finds the additional management commands
provided by *django-boost*.

The next time you invoke *./manage.py help* you should be able to see all the
newly available commands.

Optional applications
^^^^^^^^^^^^^^^^^^^^^^

Some features ship as separate, opt-in applications under ``django_boost.contrib``.
Add the ones you need alongside ``django_boost``::

  INSTALLED_APPS = [
      ...
      'django_boost',
      'django_boost.contrib.admin_tools',
  ]

``django_boost.contrib.admin_tools`` provides the ``listsuperuser`` command. The
legacy ``'django_boost.admin_tools'`` path still works but is deprecated and will
be removed in django-boost 4.0.
