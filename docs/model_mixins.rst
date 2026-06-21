Model mixins
=========================

:synopsis: Model mixins in django-boost


UUIDModelMixin
---------------

Mixins that replace ``id`` from ``AutoField`` to ``UUIDField``

::

  from django.db import models
  from django_boost.models import UUIDModelMixin

  class Stock(UUIDModelMixin):
      name = models.CharField(max_length=128)
      count = models.IntegerField()


TimeStampModelMixin
--------------------

::

  from django.db import models
  from django_boost.models.mixins import TimeStampModelMixin

  class Stock(TimeStampModelMixin):
      name = models.CharField(max_length=128)
      count = models.IntegerField()

The fields ``posted_at`` and ``updated_at`` are added.

The following fields are automatically added to the above model.

::

  posted_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


Combine
^^^^^^^^
::

  from django.db import models
  from django_boost.models.mixins import UUIDModelMixin, TimeStampModelMixin

  class Stock(UUIDModelMixin,TimeStampModelMixin):
      name = models.CharField(max_length=128)
      count = models.IntegerField()

Model mixins can also be combined in this way.

LogicalDeletionMixin
^^^^^^^^^^^^^^^^^^^^^^

::

  from django.db import models
  from django_boost.models.mixins import LogicalDeletionMixin

  class Store(LogicalDeletionMixin):
      name = models.CharField(max_length=128)

The field ``deleted_at`` is added to hold the date of the logical deletion.

Also, some methods are provided to distinguish between logically deleted items.

By default, the deletion process for models that inherit from this class is a logical deletion.

If you want to do physical deletion, please pass ``hard=True`` as a ``delete`` method argument.

Logical deletion follows Django's deletion collector for normal ``delete`` behavior:
``CASCADE``, ``PROTECT``, ``SET_NULL``, delete signals, queryset restrictions, and
the ``(count, details)`` return value are preserved. Related models that do not inherit
``LogicalDeletionMixin`` are physically deleted when Django's cascade handling deletes them,
because they have no ``deleted_at`` field to update.

::

  Store.objects.delete() # logical deletion.

  Store.objects.delete(hard=True) # physical deletion.

If you want to specify when the object was logically deleted, pass ``deleted_at``.
This is available on model instances, querysets, and managers.

::

  from django.utils.timezone import now

  deleted_at = now()

  store.delete(deleted_at=deleted_at)
  Store.objects.filter(name="Store 1").delete(deleted_at=deleted_at)
  Store.objects.delete(deleted_at=deleted_at)


``all`` method will get all the data as usual, including the logically deleted items.

To retrieve items that have not been logically removed, you can use the ``alive`` method.

If you want to retrieve only the logically deleted items, you can use the ``dead`` method.

::

  Store.objects.alive() # get not logically deleted items queryset.

  Store.objects.dead() # get logically deleted items queryset.
