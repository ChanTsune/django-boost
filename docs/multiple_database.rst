Multiple databases
==================

:synopsis: Route Django apps to separate databases

``django_boost.db.router.DatabaseRouter`` is a small app-label based database
router. Use it when whole Django apps should be assigned to specific database
aliases while the rest of the project stays on ``default``.

Configuration
-------------

Add every database alias to ``DATABASES``, enable the router, and map app labels
to database aliases with ``DATABASE_APPS_MAPPING``::

  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
      },
      'reports': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': os.path.join(BASE_DIR, 'reports.sqlite3'),
      },
  }

  DATABASE_ROUTERS = ['django_boost.db.router.DatabaseRouter']

  DATABASE_APPS_MAPPING = {
      'billing': 'default',
      'reports': 'reports',
      'audit_log': 'reports',
  }

The keys in ``DATABASE_APPS_MAPPING`` are Django app labels, not model names or
dotted Python paths. In most projects the label is the final component of the
app package name, but a custom ``AppConfig.label`` can override it.

Routing behavior
----------------

With the configuration above:

* models in the ``reports`` and ``audit_log`` apps use the ``reports`` database;
* models in the ``billing`` app use the ``default`` database explicitly;
* apps that are not listed are left to Django's normal routing behavior, which
  uses ``default`` when no other router chooses a database;
* mapped apps migrate only on their configured database;
* unmapped apps migrate on ``default`` and are not created on mapped
  non-default databases.

This router works at app granularity. If one app needs to split different
models across different databases, use separate apps or write a custom Django
database router for that policy.

Migrations
----------

Django runs migrations for one database at a time. Run migrations for
``default`` as usual, then run them for each additional alias that contains
mapped apps::

  python manage.py migrate
  python manage.py migrate --database=reports

For the example configuration, the ``reports`` and ``audit_log`` migrations run
on ``reports``. Unmapped apps such as Django's ``auth`` and ``sessions`` stay on
``default``.

System checks
-------------

django-boost registers checks for common configuration mistakes when
``django_boost`` is in ``INSTALLED_APPS``. Run them with::

  python manage.py check --tag django_boost

The checks warn when ``DATABASE_APPS_MAPPING`` is missing or names an app label
that is not installed, and report an error when it is not a dict or points to an
unknown database alias. See :doc:`checks` for the full list of check IDs.
