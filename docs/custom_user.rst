Custom User
=========================

:synopsis: django-boost custom user


EmailUser
----------

.. deprecated:: 3.2
   ``EmailUser`` and ``AbstractEmailUser`` are deprecated and will be removed in
   django-boost 4.0. Copy the model into one of your own apps and drop the
   django_boost dependency. See `Migrating off EmailUser`_.


Configuration
^^^^^^^^^^^^^

Setting of your Django project *settings.py* file.

::

  AUTH_USER_MODEL = 'django_boost.EmailUser'


Replace Django default user model.

Use email address instead of username when logging in.


AbstractEmailUser
-----------------

Available when you want to add a field to ``EmailUser``.

Inherit ``AbstractEmailUser`` and add fields.

example::

  from django.db import models
  from django_boost.models import AbstractEmailUser

  class CustomUser(AbstractEmailUser):
      is_frozen = models.BooleanField(default=False)
      homepage = models.URLField()


Migrating off EmailUser
-----------------------

``EmailUser`` is a swappable ``AUTH_USER_MODEL``. The underlying table is
``django_boost_emailuser``; keep that table name and you move **no data**.

1. Add an equivalent model to one of *your own* apps (a fresh app is simplest).
   Keep ``db_table`` so the existing table matches:

   ::

     # accounts/models.py
     from django.contrib.auth.models import AbstractUser
     from django.contrib.auth.validators import UnicodeUsernameValidator
     from django.db import models

     class User(AbstractUser):
         username = models.CharField(
             'username', max_length=150,
             validators=[UnicodeUsernameValidator()])   # non-unique: matches the existing table
         email = models.EmailField('email address', unique=True)
         USERNAME_FIELD = 'email'
         REQUIRED_FIELDS = ['username']

         class Meta(AbstractUser.Meta):
             db_table = 'django_boost_emailuser'

   ``EmailUser`` overrides ``username`` without ``unique=True``, so the existing
   table has no unique index on it; declaring it unique here would make your
   (faked) migration state claim a constraint the table lacks.

2. In *accounts/apps.py*, set ``AppConfig.default_auto_field =
   'django.db.models.AutoField'``. The existing table's ``id`` column is a
   32-bit ``AutoField``; Django's default (``BigAutoField``) would make your
   (faked) migration state claim a ``BIGINT`` column where the table has
   ``INT`` — the same class of drift as the username issue.

3. ``python manage.py makemigrations accounts`` (creates ``0001_initial``).

4. In *settings.py*: ``AUTH_USER_MODEL = 'accounts.User'``.

5. ``python manage.py migrate_emailuser``

   The command adopts the existing content type (so assigned permissions carry
   over), records your app's initial migration as applied (the table already
   exists), then runs ``migrate``.

.. note::

   Do not use ``migrate accounts 0001 --fake`` by hand. ``migrate`` runs its
   consistency check before reading ``--fake``; once ``AUTH_USER_MODEL`` points
   at the new app, ``django.contrib.admin``'s applied migration depends on your
   (unapplied) initial migration and Django raises
   ``InconsistentMigrationHistory``. ``migrate_emailuser`` records the migration
   directly, which is why it is needed.
