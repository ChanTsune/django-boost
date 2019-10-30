Path Converters
================

:synopsis: path converter keywords in django-boost


Enable path converter keywords
------------------------------
::

  from django_boost.urls import register_boost_converters

  register_boost_converters()


Example
---------
::

  from django.urls import path
  from django_boost.urls import register_boost_converters

  register_boost_converters()

  urlpatterns = [
      path('bin/<bin:id>', ~~),
      path('oct/<bin:id>', ~~),
      path('hex/<bin:id>', ~~),
  ]

Keywords
---------

bin
~~~~

``bin`` matches regular expression ``[01]+``

This is passed as `int` type to the python program.

oct
~~~~

``oct`` match ``[0-7]+``

This is passed as `int` type to the python program.

hex
~~~~

``hex`` match ``[0-9a-fA-F]``

This is passed as `int` type to the python program.

bin_str
~~~~~~~

Basically the same as ``bin``.
The difference is that it is passed to the Python program as ``str``

oct_str
~~~~~~~

Basically the same as ``oct``.
The difference is that it is passed to the Python program as ``str``

hex_str
~~~~~~~

Basically the same as ``hex``.
The difference is that it is passed to the Python program as ``str``
