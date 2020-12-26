Generic Views
=============

:synopsis: Generic view class in django-boost


Extended Views
---------------

::

  from django_boost.views.generic import View

  class YourView(View):

      def setup(self, request, *args, **kwargs):
          super().setup(request, *args, **kwargs)
          ## some process before view process

          ## For example, add attribute to view class

      def after_view_process(self, request, response, *args, **kwargs):
          super().after_view_process(request, response, *args, **kwargs)
          ## some process after view process

          ## For example, add http headers to the response

          return response

django_boost generic view (``CreateView``, ``DeleteView``, ``DetailView``, ``FormView``, ``ListView``, ``TemplateView``, ``UpdateView``, ``View``) classes has ``setup`` and ``after_view_process`` method, These are called before and after processing of View respectively.

``setup`` method is same as the method added in Django 2.2 .

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
