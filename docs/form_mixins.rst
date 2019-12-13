Form Mixins
=============

:synopsis: Form mixin class in django-boost


MatchedObjectGetMixin
----------------------

Mixin to add a method to get the queryset and object of the condition that matches the form input content.

::

  from django import forms
  from django_boost.forms.mixins import MatchedObjectGetMixin
  from .models import Customer

  class CustomerForm(MatchedObjectGetMixin, forms.ModelForm):
      class Meta:
          models = Customer
          fields = ('name', )
          field_lookup = {'name' : 'name__startswith'} # filter lookup kwargs


Set ``field_lookup`` to set detailed search conditions.

::

  from django.views.generic import FormView
  from .forms import CustomerForm

  class CustomerSearchView(FormView):
      template_name = "form.html"
      form_class = CustomerForm

      def form_valid(self,form):
          object = form.get_object()  # get matched model object
          object_list = form.get_list()  # get matched models objects queryset


``MatchedObjectMixin`` provides ``get_object`` and ``get_list`` methods, each of which returns a ``model object`` or ``queryset`` that matches the form input content.

RelatedModelInlineMixin
------------------------

Mixin that treat two related ``Model``'s as a single ``Model``.

::

  class ModelA(models.Model):
      text = models.TextField(...)


  class ModelB(models.Model):
      name = models.CharField(...)
      model_a = models.OneToOneField(to=ModelA, ...)


Specify the source field name as the dictionary key and the destination field as the dictionary value.

The dictionary value must be a ``list`` or ``tuple``.

::

  class ModelBForm(RelatedModelInlineMixin, forms.ModelForm):
      inline_fields = {'model_a': ('text',)}

      class Meta:
          model = ModelB
          fields = ('name', )

Also can inline multiple relationships.

::

  class MyModelForm(RelatedModelInlineMixin, forms.ModelForm):
      inline_fields = {'model_a': ('text',),
                       'model_x': ('text',)}

      class Meta:
          model = MyModel
          fields = ('name', )

.. autoclass:: django_boost.forms.mixins.FieldRenameMixin

