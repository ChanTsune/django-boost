Utilty Functions
=================

:synopsis: Utilty functions in django-boost


loop utils
-----------

Django Template like forloop
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
loop
~~~~~

::

  from django_boost.utils import loop

  for forloop, item in loop([1, 2, 3, 4, 5]):
      forloop.counter0
      forloop.counter
      forloop.revcounter0
      forloop.revcounter
      forloop.first
      forloop.last

Provides Django Template loops to Python programs.

loopfirst
~~~~~~~~~~

Yield True when the first element of the given iterator object, False otherwise.

::

  from django_boost.utils.functions import loopfirst

  for is_first, v in loopfirst(range(5)):
      print(is_first, v)

  # True 0
  # False 1
  # False 2
  # False 3
  # False 4

looplast
~~~~~~~~~

Yield True when the last element of the given iterator object, False otherwise.

::

  from django_boost.utils.functions import looplast

  for is_last, v in looplast(range(5)):
      print(is_last, v)

  # False 0
  # False 1
  # False 2
  # False 3
  # True 4

loopfirstlast
~~~~~~~~~~~~~~

A function combining ``firstloop`` and ``lastloop``.

Yield True if the first and last element of the iterator object, False otherwise.

::

  from django_boost.utils.functions import loopfirstlast

  for first_or_last, v in loopfirstlast(range(5)):
      print(first_or_last, v)

  # True 0
  # False 1
  # False 2
  # False 3
  # True 4
