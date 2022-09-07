.. django-boost documentation master file, created by
   sphinx-quickstart on Sun Oct 20 15:56:03 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-boost's documentation!
========================================

Django Boost is a collection of custom extensions for the Django Framework.

These include management commands, additional database fields,
admin extensions, view mixins, form mixins and much more.


Getting Started
===============

Getting it
==========

You can get Django Boost by using pip::

 $ pip install django-boost

If you want to install it from source, grab the git repository and run setup.py::

 $ git clone git://github.com/ChanTsune/django-boost.git
 $ python setup.py install

For more detailed instructions check out our :doc:`installation_instructions`.
Enjoy.

Compatibility with versions of Python and Django
=================================================

We follow the Django guidelines for supported Python and Django versions.

See more at `Django Supported Versions <https://docs.djangoproject.com/en/dev/internals/release-process/#supported-versions>`_

This might mean the django-boost may work with older or unsupported versions but we do not guarantee it and most likely will not fix bugs related to incompatibilities with older versions.

At this time we test on and thrive to support valid combinations of Python 3.8, 3.9, 3.10 and pypy3 with Django versions 3.0 to 3.2 and 4.0.



.. toctree::
   :maxdepth: 3
   :caption: Contents:

   installation_instructions
   custom_user
   model_mixins
   model_fields
   multiple_database
   middleware
   http_status_code_exceptions
   generic_views
   view_mixins
   form
   form_mixins
   form_fields
   path_converters
   shortcut_functions
   routing_utilitys
   admin_site_utilitys
   utility_functions
   template_context
   template_tags
   commands


Indices and tables
==================

* :ref:`search`
