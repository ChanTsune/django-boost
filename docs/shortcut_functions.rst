Shortcut Functions
===================

:synopsis: Model mixins in django-boost


::

  from django_boost.shortcuts import (
      get_list_or_default, get_list_or_exception,
      get_object_or_default, get_object_or_exception)

  my_model = MyModel.objects.get(id=1)
  get_object_or_default(MyModel, default=my_model, id=2)

  get_object_or_exception(MyModel, exception=Exception, id=2)


These behave like ``get_object_or_404``
