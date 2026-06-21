Model fields
=========================

:synopsis: Model fields in django-boost

JsonField
----------

.. warning::

  ``django_boost.models.fields.JsonField`` is deprecated and will be removed in
  django-boost 3.0. Use Django's native ``django.db.models.JSONField`` instead,
  available since Django 3.1.

Existing projects that store JSON through the legacy text-based field should
plan a schema and data migration to Django's native ``JSONField`` before
upgrading to django-boost 3.0.

AutoOneToOneField
------------------

::

  from django.db import models
  from django_boost.models.fields import AutoOneToOneField

  class UserProfile(models.Model):
      user = AutoOneToOneField(User, primary_key=True, related_name='profile')
      home_page = models.URLField(max_length=255, blank=True)

``AutoOneToOneField`` automatically created when the target model instance does not exist when reverse access.

In the above case, when the `UserProfile` model is referenced from the `User` model,
a `UserProfile` instance is automatically created when there is no `UserProfile` model associated with the `User` model.

ColorCodeField
---------------

::

  from django.db import models
  from django_boost.models.fields import ColorCodeField

  class MyModel(models.Model):
      color = ColorCodeField()


Save hexadecimal color code string including #.

If you specify ``upper=True``, the saved text will be capitalized.

On the other hand, specifying ``lower=True`` will make the saved string lower case.

You can not specify both at the same time.

If neither is set, the string is saved without any changes.

Default is ``upper=False``, ``lower=Flase``.


SplitDateTimeField
-------------------

::

  from django.db import models
  from django_boost.models.fields import SplitDateTimeField

  class MyModel(models.Model):
      date = SplitDateTimeField()

A little convenient DateTimeField.

``SplitDateTimeField`` is the form_class of ``django.models.db.DateTimeField`` replaced with ``django.forms.SplitDateTimeField``.

Internal DB field is the same as ``django.models.db.DateTimeField``.
