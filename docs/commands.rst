Commands
=========

:synopsis: 

adminsitelog
-------------

::

  $ python manage.py adminsitelog

View and delete Admin Site logs.

view all logs
~~~~~~~~~~~~~~

::

  $ python manage.py adminsitelog

::

  id| action | detail | user | time
  6 | Deleted | Customer object (8) | admin | 2019-08-19 14:56:29.609940+00:00
  7 | Added | Customer object (11) | admin | 2019-08-20 16:12:38.902129+00:00
  8 | Changed | Customer object (4) - Changed color. | admin | 2019-08-20 16:12:45.653693+00:00

filter logs
~~~~~~~~~~~~

::

  $ python manage.py adminsitelog --filter "action_time>=2019-8-01" --exclude "id=6"

::

  id | action | detail | user | time
  7 | Added | Customer object (11) | admin | 2019-08-20 16:12:38.902129+00:00
  8 | Changed | Customer object (4) - Changed color. | admin | 2019-08-20 16:12:45.653693+00:00


delete all logs
~~~~~~~~~~~~~~~~

::

  $ python manage.py adminsitelog --delete

It is also possible to delete only the logs narrowed down by ``--filter`` and ``--exclude``.


support_heroku
---------------

::

  $ python manage.py support_heroku


Create heroku config files.
``Procfile``, ``runtime.txt``, ``requirements.txt``

For more details.

::

  $ python manage.py support_heroku -h
