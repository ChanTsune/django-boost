Validators
==========

:synopsis: Validator classes and functions in django-boost

Validators for form and model fields. Use them like Django's built-in
validators, by passing them in a field's ``validators`` argument.


ContainAnyValidator
-------------------

Validate that the input contains at least one of the given elements.

::

  from django import forms
  from django_boost.validators import ContainAnyValidator

  class SignUpForm(forms.Form):
      password = forms.CharField(
          validators=[ContainAnyValidator("0123456789")])

The elements may be any iterable; a value passes when it shares at least one
element with it.


ColorCodeValidator / validate_color_code
----------------------------------------

Validate that the whole value is a 6-digit hexadecimal color code prefixed
with ``#`` (e.g. ``#00ff88``).

::

  from django.db import models
  from django_boost.validators import validate_color_code

  class Theme(models.Model):
      accent = models.CharField(max_length=7, validators=[validate_color_code])

``validate_color_code`` is a ready-made instance; use the ``ColorCodeValidator``
class when you want a custom message.


JsonValidator / validate_json
-----------------------------

Validate that the value is a JSON-parseable string.

::

  from django_boost.validators import validate_json

  validate_json('{"a": 1}')   # ok
  validate_json('{a: 1}')     # raises ValidationError


NonZeroValidator / validate_non_zero
------------------------------------

Validate that an integer is not ``0``. Django's ``MinValueValidator`` /
``MaxValueValidator`` cover the other integer ranges; excluding only zero is
the one range they cannot express as a single validator.

::

  from django.db import models
  from django_boost.validators import validate_non_zero

  class Transfer(models.Model):
      amount = models.IntegerField(validators=[validate_non_zero])

Use the ``NonZeroValidator`` class to supply a custom message.


validate_uuid4
--------------

.. deprecated:: 3.1.0
   ``validate_uuid4`` will be removed in django-boost 4.0. Validate UUIDs with
   Django's ``UUIDField`` or ``uuid.UUID`` instead.
