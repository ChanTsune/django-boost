Form Fields
=============

:synopsis: Form field class in django-boost


ColorCodeField
----------------------

Field for storing hexadecimal color code like ``#FFEEDD``.

::

  from django import forms
  from django_boost.forms.fields import ColorCodeField

  class MyForm(forms.Form):
      color = ColorCodeField()


InvertBooleanField
----------------------

Field that returns inverted input.

Returns false if the checkbox is checked, returns true if the checkbox is not checked.

::

  from django import forms
  from django_boost.forms.fields import InvertBooleanField

  class MyForm(forms.Form):
      invert = InvertBooleanField()
