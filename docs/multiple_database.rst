Multiple database
=========================

:synopsis: Use multiple database

Use multiple database
------------------------

Switch the database used for each application.

settings.py ::

  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
      },
      'db2': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': os.path.join(BASE_DIR, 'db2.sqlite3'),
      }
  }

  DATABASE_ROUTERS = ['django_boost.db.router.DatabaseRouter']

  DATABASE_APPS_MAPPING = {
      "myapp" : "db2",
      "myapp2" : "db2"
  }

In the above example, application `myapp` and `myapp2` will use the database `db2`.

Other applications use the default database.
