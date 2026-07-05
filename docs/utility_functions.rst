Utility Functions
=================

:synopsis: Utility functions in django-boost


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

Provides Django Template loops to Python programs. ``loop()`` wraps *iterable*
in a ``Loop`` instance (the ``forloop`` object above).

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

Combine ``loopfirst`` and ``looplast``.

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


type utils
-----------

isiterable
~~~~~~~~~~~

::

  from django_boost.utils import isiterable

  isiterable([1, 2, 3])  # True
  isiterable(1)          # False

Return `True` if `obj` is iterable object, `False` otherwise.

contain_any
~~~~~~~~~~~~

::

  from django_boost.utils import contain_any

  contain_any([1, 2, 3], [3, 4, 5])  # True
  contain_any([1, 2, 3], [4, 5])     # False

Return `True` if any of the `elements` are contained in `container`, `False`
otherwise.


itertools utils
-----------------

take
~~~~~

::

  from django_boost.utils.itertools import take

  take(3, range(10))  # [0, 1, 2]

Return first *n* items of the iterable as a list.

chunked
~~~~~~~~

::

  from django_boost.utils.itertools import chunked

  list(chunked([1, 2, 3, 4, 5, 6], 3))  # [[1, 2, 3], [4, 5, 6]]

Break *iterable* into lists of length *n*.


json utils
-----------

model_to_json
~~~~~~~~~~~~~~

::

  from django_boost.utils.functions import model_to_json

  model_to_json(my_model_instance)          # {'id': 1, 'name': 'x', ...}
  model_to_json(MyModel.objects.filter())   # [{'id': 1, ...}, {'id': 2, ...}]

Take a Model instance or QuerySet and return a dict, or a list of dicts,
of its field values.

json_to_model
~~~~~~~~~~~~~~

::

  from django_boost.utils.functions import json_to_model

  json_to_model(MyModel, model_to_json(my_model_instance))

Build an unsaved ``MyModel`` instance from a dict shaped like
``model_to_json``'s output.
