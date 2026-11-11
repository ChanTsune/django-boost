Generic Views
=============

:synopsis: Generic view class in django-boost


JsonView
---------

.. autoclass:: django_boost.views.generic.JsonView

StringView
-----------

.. autoclass:: django_boost.views.simple.StringView


ModelCRUDViews
---------------

Provides easy creation of CRUDViews linked to model.

::

  from django_boost.views.generic import ModelCRUDViews

  class CustomerViews(ModelCRUDViews):
      model = Customer

::

  from django.urls import path, include
  from . import views

  urlpatterns = [
      path('views/', include(views.CustomerViews().urls)),
  ]

In the template you can use as follows.

::

  {% url 'customer:list' %}
  {% url 'customer:create' %}
  {% url 'customer:detail' %}
  {% url 'customer:update' %}
  {% url 'customer:delete' %}

The name of the URL is defined under the namespace of the lower-cased model class name.  

Case of Namespaced
~~~~~~~~~~~~~~~~~~~

::

  from django.urls import path, include
  from . import views

  app_name = "myapp"
  urlpatterns = [
      path('views/', include(views.CustomerViews(app_name="myapp:customer").urls)),
  ]

In the template you can use as follows.

::

  {% url 'myapp:customer:list' %}
  {% url 'myapp:customer:create' %}
  {% url 'myapp:customer:detail' %}
  {% url 'myapp:customer:update' %}
  {% url 'myapp:customer:delete' %}
