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
      path('oct/<oct:id>', ~~),
      path('hex/<hex:id>', ~~),
      path('float/<float:id>', ~~),
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

``hex`` match ``[0-9a-fA-F]+``

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

float
~~~~~~~

``float`` match ``'[0-9]+([.][0-9]+)?'``

This is passed as ``float`` type to the python program.

date
~~~~~~

``date`` matches dates that consider leap years like ``'Y/m/d'``

This is passed as ``datetime.datetime`` type to python program.

signed_int
~~~~~~~~~~

``signed_int`` matches ``-?[0-9]+`` (any integer, including negatives).

This is passed as ``int`` type to the python program.

positive_int
~~~~~~~~~~~~

``positive_int`` matches integers greater than ``0``.

This is passed as ``int`` type to the python program.

negative_int
~~~~~~~~~~~~

``negative_int`` matches integers less than ``0``.

This is passed as ``int`` type to the python program.

non_negative_int
~~~~~~~~~~~~~~~~

``non_negative_int`` matches integers greater than or equal to ``0``.

This is passed as ``int`` type to the python program.

non_positive_int
~~~~~~~~~~~~~~~~

``non_positive_int`` matches integers less than or equal to ``0``.

This is passed as ``int`` type to the python program.

non_zero_int
~~~~~~~~~~~~

``non_zero_int`` matches non-zero integers.

This is passed as ``int`` type to the python program.
