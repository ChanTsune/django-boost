Commands
=========

:synopsis: Exist commands in django-boost

adminsitelog
-------------

::

  $ python manage.py adminsitelog

View and delete Admin Site logs.

::

  usage: manage.py adminsitelog [-h] [--version] [-v {0,1,2,3}]
                                [--settings SETTINGS] [--pythonpath PYTHONPATH]
                                [--traceback] [--no-color] [-d]
                                [--filter FILTER [FILTER ...]]
                                [--exclude EXCLUDE [EXCLUDE ...]]
                                [--order_by ORDER_BY [ORDER_BY ...]]
                                [--name_field NAME_FIELD]

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

::

  usage: manage.py support_heroku [-h] [--overwrite] [--no-gunicorn] [--runtime]
                                  [--prockfile]
                                  [--release RELEASE [RELEASE ...]]
                                  [--requirments] [-q] [--version]
                                  [-v {0,1,2,3}] [--settings SETTINGS]
                                  [--pythonpath PYTHONPATH] [--traceback]
                                  [--no-color] [--force-color] [--skip-checks]

  Create a configuration file for heroku `Procfile`,`runtime.txt` and
  `requirements.txt`

  optional arguments:
    -h, --help            show this help message and exit
    --overwrite           Overwrite even if file exists.
    --no-gunicorn         Don't automatically add `gunicorn` to
                          `requirements.txt`.
    --runtime             Create only `runtime.txt`, By default all files are
                          created.
    --prockfile           Create only `Prockfile`, By default all files are
                          created.
    --release RELEASE [RELEASE ...]
                          Add the command to be executed in the release phase to
                          `Prockfile`
    --requirments         Create only `requirments.txt`, By default all files
                          are created.
    -q, --quit            Don't output to standard output.
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
    --skip-checks         Skip system checks.


deletemigrations
---------------
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
