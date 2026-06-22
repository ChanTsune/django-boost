Template
========

:synopsis: template utilities in django-boost

Strict invalid template variables
---------------------------------

``StrictInvalidTemplateVariable`` raises an exception when a Django template
tries to render an invalid or missing variable.

It provides Jinja2 ``StrictUndefined``-like behavior for Django templates,
which is useful when you want missing template variables to fail fast instead
of rendering as empty strings.

Use it as Django's ``string_if_invalid`` template option::

  from django_boost.template import StrictInvalidTemplateVariable

  TEMPLATES = [
      {
          "BACKEND": "django.template.backends.django.DjangoTemplates",
          "DIRS": [],
          "APP_DIRS": True,
          "OPTIONS": {
              "string_if_invalid": StrictInvalidTemplateVariable(),
          },
      },
  ]

By default, missing variables raise ``ValueError`` with the missing template
variable name in the message.

You can customize the message or exception class::

  class TemplateVariableError(Exception):
      pass


  TEMPLATES = [
      {
          "BACKEND": "django.template.backends.django.DjangoTemplates",
          "APP_DIRS": True,
          "OPTIONS": {
              "string_if_invalid": StrictInvalidTemplateVariable(
                  message="Missing template variable: {name}",
                  exception_class=TemplateVariableError,
              ),
          },
      },
  ]

Limitations
-----------

``StrictInvalidTemplateVariable`` only raises on the resolution path Django
routes through ``string_if_invalid % var``. It does not cover every invalid
lookup, so unlike Jinja2 ``StrictUndefined`` it is not strict everywhere:

- Tags that resolve variables while ignoring failures -- ``{% if %}``,
  ``{% for %}``, ``{% firstof %}`` and the like -- never reach it, so a missing
  variable there is still treated as falsy/empty instead of raising.
- A method marked ``alters_data`` or one that requires arguments yields
  Django's invalid marker without the ``%`` step, so it renders the literal
  ``%s`` rather than raising.
