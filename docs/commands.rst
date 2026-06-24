Commands
=========

:synopsis: Exist commands in django-boost

adminsitelog
-------------

::

  $ python manage.py adminsitelog

View and delete Admin Site logs.

.. note::

   ``adminsitelog`` ships in the optional ``django_boost.contrib.admin_tools``
   application (see :doc:`installation_instructions`) and also requires
   ``django.contrib.admin``; without it the command exits with an error.
   Running ``adminsitelog`` through ``django_boost`` alone still works but is
   deprecated and will be removed in django-boost 4.0.

::

  usage: manage.py adminsitelog [-h] [--version] [-v {0,1,2,3}]
                                [--settings SETTINGS] [--pythonpath PYTHONPATH]
                                [--traceback] [--no-color] [-d]
                                [--filter FILTER [FILTER ...]]
                                [--exclude EXCLUDE [EXCLUDE ...]]
                                [--order_by ORDER_BY [ORDER_BY ...]]
                                [--name_field NAME_FIELD]
                                [--format {text,csv,tsv}]

  Django admin site log

  optional arguments:
    -h, --help            show this help message and exit
    --version             show program's version number and exit
    -v {0,1,2,3}, --verbosity {0,1,2,3}
                          Verbosity level; 0=minimal output, 1=normal output,
                          2=verbose output, 3=very verbose output
    --settings SETTINGS   The Python path to a settings module, e.g.
                          "myproject.settings.main". If this isn't provided, the
                          DJANGO_SETTINGS_MODULE environment variable will be
                          used.
    --pythonpath PYTHONPATH
                          A directory to add to the Python path, e.g.
                          "/home/djangoprojects/myproject".
    --traceback           Raise on CommandError exceptions
    --no-color            Don't colorize the command output.
    -d, --delete          Delete displayed logs.
    --filter FILTER [FILTER ...]
                          Filter the Log to be displayed. Supported filed is
                          action_flag, action_time, change_message,
                          content_type, content_type_id, id, object_id,
                          object_repr, user, user_id. e.g.
                          "action_time>=2019-8-22"
    --exclude EXCLUDE [EXCLUDE ...]
                          Exclude the Log to be displayed. Supported filed is
                          same as --filter. e.g. "user__username=admin"
    --order_by ORDER_BY [ORDER_BY ...]
                          Order of Log to be displayed. Supported filed is
                          action_flag, action_time, change_message,
                          content_type, content_type_id, id, object_id,
                          object_repr, user, user_id. e.g. "-action_flag"
    --name_field NAME_FIELD
                          user name field. e.g. "--name_field email", "--
                          name_field profile.phone"
    --format {text,csv,tsv}
                          Output format.

view all logs
~~~~~~~~~~~~~~

::

  $ python manage.py adminsitelog

::

  id | action | detail | user | time
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


output csv/tsv
~~~~~~~~~~~~~~

::

  $ python manage.py adminsitelog --format csv

::

  id,action,detail,user,time
  7,Added,Customer object (11),admin,2019-08-20 16:12:38.902129+00:00
  8,Changed,Customer object (4) - Changed color.,admin,2019-08-20 16:12:45.653693+00:00

Use ``--format tsv`` to output tab-separated values.


delete all logs
~~~~~~~~~~~~~~~~

::

  $ python manage.py adminsitelog --delete

It is also possible to delete only the logs narrowed down by ``--filter`` and ``--exclude``.


deletemigrations
-----------------
::

  $ python manage.py deletemigrations appname

Delete migration files.

::

  usage: manage.py deletemigrations [-h] [-y] [--version] [-v {0,1,2,3}]
                                    [--settings SETTINGS]
                                    [--pythonpath PYTHONPATH] [--traceback]
                                    [--no-color] [--force-color]
                                    app_label [app_label ...]

  delete migration files.

  positional arguments:
    app_label             One or more application label.

  optional arguments:
    -h, --help            show this help message and exit
    -y
    --version             show program's version number and exit
    -v {0,1,2,3}, --verbosity {0,1,2,3}
                          Verbosity level; 0=minimal output, 1=normal output,
                          2=verbose output, 3=very verbose output
    --settings SETTINGS   The Python path to a settings module, e.g.
                          "myproject.settings.main". If this isn't provided, the
                          DJANGO_SETTINGS_MODULE environment variable will be
                          used.
    --pythonpath PYTHONPATH
                          A directory to add to the Python path, e.g.
                          "/home/djangoprojects/myproject".
    --traceback           Raise on CommandError exceptions
    --no-color            Don't colorize the command output.
    --force-color         Force colorization of the command output.

listsuperuser
-------------
::

  $ python manage.py listsuperuser

List the project's super users together with audit-relevant fields: their
email, whether the account is active, whether it is staff, and the last login
time. Inactive super users are listed too, so stale privileged accounts stay
visible.

::

  $ python manage.py listsuperuser
  email | active | staff | last_login
  admin@example.com | yes | yes | 2026-06-20 09:12:01+00:00
  old-root@example.com | no | yes | (never)

Use ``--format csv`` or ``--format tsv`` for machine-readable output::

  $ python manage.py listsuperuser --format csv
  email,active,staff,last_login
  admin@example.com,yes,yes,2026-06-20 09:12:01+00:00
  old-root@example.com,no,yes,(never)

.. note::

   ``listsuperuser`` ships in the optional ``django_boost.contrib.admin_tools``
   application (see :doc:`installation_instructions`). Installing it under the
   legacy ``'django_boost.admin_tools'`` ``INSTALLED_APPS`` entry still works
   but warns on startup; switch the entry to
   ``'django_boost.contrib.admin_tools'``. The legacy entry will be removed in
   django-boost 4.0.
