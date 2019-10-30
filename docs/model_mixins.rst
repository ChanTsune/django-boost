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

