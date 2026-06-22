Django system checks
====================

:synopsis: Django system checks provided by django-boost

django-boost registers its checks automatically when ``django_boost`` is in
``INSTALLED_APPS``.

Run all Django checks with::

  python manage.py check

Run only django-boost checks with::

  python manage.py check --tag django_boost

Check IDs
---------

``django_boost.W001``
  ``django_boost.db.router.DatabaseRouter`` is configured, but
  ``DATABASE_APPS_MAPPING`` is missing. Set ``DATABASE_APPS_MAPPING`` to a dict
  mapping app labels to database aliases.

``django_boost.E001``
  ``DATABASE_APPS_MAPPING`` is not a dict. Set it to a dict such as
  ``{"myapp": "secondary"}``.

``django_boost.E002``
  ``DATABASE_APPS_MAPPING`` references a database alias that is not present in
  ``DATABASES``. Add the alias to ``DATABASES`` or update the mapping.

``django_boost.W002``
  ``DATABASE_APPS_MAPPING`` contains an app label that is not installed. Use the
  app label from the app's ``AppConfig``.

``django_boost.W010``
  ``RedirectCorrectHostnameMiddleware`` is enabled with ``DEBUG = False``, but
  ``CORRECT_HOST`` is missing or empty. Set ``CORRECT_HOST`` to the canonical
  host name or remove the middleware.

``django_boost.W011``
  ``CORRECT_HOST`` appears to contain a scheme, path, or whitespace. Set it to a
  host name such as ``"example.com"`` or ``"www.example.com"``.

``django_boost.W012``
  ``CORRECT_HOST`` is not allowed by ``ALLOWED_HOSTS`` when ``DEBUG = False``.
  Add the canonical host to ``ALLOWED_HOSTS``. A wildcard ``"*"`` is accepted.
  If ``CORRECT_HOST`` includes a port, django-boost compares the host name
  portion against ``ALLOWED_HOSTS`` like Django does for incoming requests.

``django_boost.E020``
  ``django_boost.context_processors.user_agent`` is configured, but the optional
  ``user-agents`` dependency is not installed. Install it with
  ``pip install django-boost[useragent]``.

  This check detects the context processor configuration. It does not attempt to
  statically detect arbitrary ``UserAgentMixin`` usage in view code.

``django_boost.W030``
  A model using ``LogicalDeletionMixin`` is missing the ``deleted_at`` field.
  Keep the inherited field or provide a nullable replacement.

``django_boost.W031``
  A model using ``LogicalDeletionMixin`` has a default manager without
  ``alive()``, ``dead()``, or ``revive()``. Keep the inherited
  ``LogicalDeletionManager`` or provide a compatible manager.

``django_boost.W032``
  A model using ``LogicalDeletionMixin`` has a non-nullable ``deleted_at``
  field. Keep the inherited field or provide a replacement that allows
  ``NULL``.
