Admin Site Utilitys
====================

:synopsis: Admin site utilitys in django-boost


register_all
------------

Easily register Models to Django admin site.

::

  from yourapp import models
  from django_boost.admin.site import register_all

  register_all(models)

Register all models defined in `models.py` in Django admin site.

Custom admin classes are also available.

::

  from your_app import models
  from your_app import admin
  from django_boost.admin.site import register_all

  register_all(models, admin_class=admin.CustomAdmin)
