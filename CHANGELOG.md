# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Version numbers follow [PEP 440](https://peps.python.org/pep-0440/).

## [Unreleased]

### Added

- `LogicalDeletionQuerySet`/`LogicalDeletionManager` gained `deleted_since`, `deleted_before`, and `deleted_between` methods for filtering by deletion date.

### Fixed

- The `Toggleswitch` widget's visible label is now clickable; its `for` attribute now matches the input's `id`.
- The `date` path converter now accepts a `datetime.date` value (e.g. from a `DateField`) in `reverse()`, instead of raising `NoReverseMatch`.
- `AnonymousRequiredMixin` views are no longer redirected to the login page by Django's `LoginRequiredMiddleware` (Django 5.1+) before the view can run.

## [3.3.1] - 2026-07-17

### Fixed

- Saving a `RelatedModelInlineMixin` form no longer discards the base model's own many-to-many field values.
- `LogicalDeletionManager` used on a model without `LogicalDeletionMixin` now performs a logical delete instead of a physical delete.
- `DynamicRedirectMixin` combined with `CreateView`/`UpdateView`/`DeleteView` now interpolates a `success_url` placeholder (e.g. `{id}`) and falls back to the object's `get_absolute_url()`, instead of returning the literal placeholder or raising `ImproperlyConfigured`.
- `AutoOneToOneField`'s auto-created related object is now created on the database the router resolves for the parent instance, instead of always the default database.

## [3.3.0] - 2026-07-16

### Added

- `LogicalDeletionModelAdmin` now includes a deletion-date filter with today, 7/30/90-day, older-than-90-day, and inclusive custom-range options.
- Decimal path converters `decimal`, `signed_decimal`, `positive_decimal`, `negative_decimal`, `non_negative_decimal`, `non_positive_decimal` and `non_zero_decimal`, covering decimal ranges Django's built-in `float` converter cannot express; `decimal` is an alias of `non_negative_decimal`.
- Float path converters `signed_float`, `positive_float`, `negative_float`, `non_negative_float`, `non_positive_float` and `non_zero_float`, symmetric with the existing signed-integer and decimal converter families; `float` is now an explicit alias of `non_negative_float` (same regex and behavior as before).

### Fixed

- Comparing two `JsonValidator` (or two `NonZeroValidator`) instances no longer raises `AttributeError`.
- The `mimetype` template filter now returns an empty string for an unknown extension (instead of the literal `None`) and accepts a non-string value instead of raising `TypeError`.
- `ReAuthenticationRequiredMixin(logout=True)` no longer returns a 405 instead of logging out on Django 5.0+.
- `LogicalDeletionMixin.revive`, `LogicalDeletionQuerySet.revive`, and `LogicalDeletionManager.delete`/`revive` can no longer be triggered by rendering a template variable, matching Django's own `delete`/`update`.

## [3.2.4] - 2026-07-11

### Fixed

- `StaticView` now responds with a 404 instead of a 500 when its file is missing at request time.
- `include_static_files` now routes each file name literally, so a name containing `<`/`>` (e.g. `<script>.js`) is no longer interpreted as a path converter that would match unrelated URLs.

## [3.2.3] - 2026-07-07

### Fixed

- `deletemigrations` now deletes only the top-level migration modules, no longer descending into subpackages under `migrations/` and removing unrelated `.py` files.
- `getattr_chain` without a default now propagates the underlying `AttributeError` instead of rewriting it into a generic one.
- The `urlencode`/`urldecode` template filters now coerce a non-string value (e.g. an int or `None`) to `str`, instead of raising `TypeError`.
- The status-code exceptions (`Http400`, `Http500`, and the rest) are now importable from `django_boost.http`, instead of only from `django_boost.http.response`.

## [3.2.2] - 2026-07-06

### Fixed

- `RelatedModelInlineMixin.save(commit=False)` no longer writes to the database; its inline related objects are now persisted by `save_m2m()`, following Django's `ModelForm` contract.
- `json_to_model` no longer raises `ValueError` for models with a relation field; it round-trips `model_to_json` output by assigning to the field's `*_id` column.
- The admin hard-delete action now logs deletions with Django 5.1+'s bulk `log_deletions()` when available, avoiding the `log_deletion()` deprecation warning.
- `get_object_or_exception` and `get_list_or_exception` now fall back to the model's `DoesNotExist` when called without an `exception`, instead of raising `TypeError` from `raise None`.

## [3.2.1] - 2026-07-05

### Fixed

- `adminsitelog` now reports an unknown `--filter`/`--exclude`/`--order_by` field name as a command error instead of an unhandled `FieldError` traceback.
- Comparing two `ContainAnyValidator` instances no longer raises `AttributeError`; `__init__` now initializes the inherited `limit_value`.
- `ContainAnyValidator` no longer raises `TypeError` when its custom message omits the `%s` placeholder; it raises `ValidationError` with the message verbatim.
- `JsonResponseMixin.get` now builds the response with the view's `response_class` instead of a hardcoded `JsonResponse`, so a custom response class takes effect.
- `ColorCodeField` now implements `deconstruct()`, so its `upper`/`lower` option is preserved in migrations instead of being dropped.

## [3.2.0] - 2026-07-04

### Added

- Signed-integer path converters `signed_int`, `positive_int`, `negative_int`, `non_negative_int`, `non_positive_int` and `non_zero_int` (registered by `register_boost_converters`), covering integer ranges Django's built-in `int` converter cannot express.
- `NonZeroValidator` and `validate_non_zero`, rejecting a value of `0` — the one integer range Django's built-in `MinValueValidator`/`MaxValueValidator` cannot express as a single validator.
- `Http505`, `Http506`, `Http508`, `Http509`, `Http510` and `Http511` exceptions, so the 5xx statuses whose response classes django-boost already ships can now be raised through `HttpStatusCodeExceptionMiddleware`, not only returned. A raised or returned `509` now carries the status message `Bandwidth Limit Exceeded` instead of an empty phrase.
- `AnonymousRequiredMixin`, a view mixin that redirects an already-authenticated user away (e.g. from a login or sign-up page) — the inverse of Django's `LoginRequiredMixin`. The redirect target is `redirect_authenticated_url`, falling back to `settings.LOGIN_REDIRECT_URL`.
- `django_boost.test.TestCase.assertStatusCodeNotIn`, completing the `assertStatusCode*` family alongside `assertStatusCodeEqual`, `assertStatusCodeNotEqual` and `assertStatusCodeIn`.

### Deprecated

- `django_boost.EmailUser` / `AbstractEmailUser` are deprecated and will be removed in 4.0. A system check (`django_boost.W050`) now warns when `AUTH_USER_MODEL` is `'django_boost.EmailUser'`. Copy the model into one of your own apps (keeping `db_table = 'django_boost_emailuser'`) and run the new `migrate_emailuser` command to adopt the existing table and its permissions. See the Custom User docs.

### Fixed

- `JsonResponseMixin.get_context_data` no longer mutates the shared class-level `extra_context`, so request-specific keyword arguments no longer leak into later requests.
- `RedirectCorrectHostnameMiddleware` no longer raises a `TypeError` on the redirect path under ASGI; it now redirects correctly on both WSGI and ASGI.
- A custom `delete_flag_field` on `LogicalDeletionManager` now survives queryset cloning, so a chained `filter(...).alive()`/`dead()`/`revive()` no longer raises `FieldError`.
- `AutoOneToOneField` reverse access on an unsaved parent now raises `RelatedObjectDoesNotExist` instead of a `ValueError`.
- `adminsitelog`'s `--filter`/`--exclude` now split each condition on its leftmost operator, so a value containing `>=` or `<=` is no longer mis-parsed.
- `looplast` and `loopfirstlast` now accept any iterable (e.g. a generator), matching `loopfirst`, instead of raising `TypeError`.
- The shipped `EmailUser` migrations now match the model: `makemigrations` no longer reports unapplied changes for `django_boost`, and `first_name` accepts up to 150 characters (its column was previously capped at 30). Run `migrate` to widen the column.

## [3.1.2] - 2026-07-03

### Fixed

- `ModelCRUDViews` create/update now works with a view that defines its own `form_class` or `fields`.
- `RelatedModelInlineMixin` no longer raises `AttributeError` when a reverse one-to-one related row does not exist yet.
- `Http405` via `HttpStatusCodeExceptionMiddleware` now returns a valid 405 with an `Allow` header set from its `permitted_methods` argument.
- `ReAuthenticationRequiredMixin` no longer raises `TypeError` for an authenticated user whose `last_login` is `None`.

## [3.1.1] - 2026-07-02

### Fixed

- The `date` path converter now accepts years below 1000 (e.g. `48/2/29`).
- The `boost_query` `filter`/`exclude` template filters now accept values containing `=`.
- `LogicalDeletionModelAdmin`'s hard-delete action no longer leaks onto other model admins on the same site.
- `JsonRequestMixin.json` now honors the request's declared charset and falls back to `{}` for an unreadable body.

## [3.1.0] - 2026-07-01

### Added

- `iter`, `list`, `dict`, `set`, `tuple` and `frozenset` filters in the
  `boost` template library, exposing the corresponding Python built-ins.
- `django_boost.test.TestCase`'s `assertStatusCode*` assertions now accept an optional `msg` argument.

### Deprecated

- The `django_boost.views` base `View` class, its `after_view_process` hook,
  and the generic-view aliases (`TemplateView`, `FormView`, `CreateView`,
  `ListView`, `DetailView`, `UpdateView`, `DeleteView`) are deprecated and will
  be removed in django-boost 4.0. Use `django.views.generic.*`, and a
  `dispatch()` override or middleware in place of `after_view_process`.
- `validate_uuid4` is deprecated and will be removed in django-boost 4.0.
  Validate UUIDs with Django's `UUIDField` or `uuid.UUID` instead.

### Fixed

- `django_boost.admin.sites.register_all` now registers the models it finds; previously it registered none.
- The `next` template filter now works for iterators without a supplied default value.
- `django_boost.forms.UserCreationForm`, `UserChangeForm`, and `AuthenticationForm` now apply Django's `UsernameField` behavior.
- `django_boost.utils.functions.model_to_json` no longer raises `AttributeError` when given a `QuerySet`.
- The `urldecode` template filter's output is now auto-escaped instead of being treated as safe HTML.
- The `upper`/`lower` option of `ColorCodeField` no longer raises `AttributeError` on a `None` value.
- `django_boost.test.TestCase`'s `assertStatusCode*` failures now point at the calling test instead of the assertion helper.
- `validate_color_code` (and `ColorCodeField`) now require the whole value to be a color code, rejecting strings that merely contain one (e.g. `"x#abcdef"`).
- The `int` template filter now accepts numeric values (int/float).
- `ContainAnyValidator` now raises `ValidationError` for invalid input when given multiple elements as a tuple.
- The `date` path converter now accepts zero-padded dates (e.g. `2020/02/29`).
- `SpaceLessMiddleware` now compresses streaming HTML responses lazily (async streams included) and works in ASGI middleware chains.
- `StaticView` with an explicit `content_type` no longer crashes with `UnboundLocalError`.
- `RedirectCorrectHostnameMiddleware` now reads `DEBUG` and `CORRECT_HOST` per request.
- `LogicalDeletionMixin.revive()` now honors its `using` and `force_update` arguments.
- A custom `delete_flag_field` on `LogicalDeletionManager` now applies to its `alive()`/`dead()`/`revive()` queries.

## [3.0.1] - 2026-06-26

### Fixed

- `SpaceLessMiddleware` no longer un-escapes HTML entities in page text.
- `SpaceLessMiddleware` no longer crashes on streaming HTML responses.
- `SpaceLessMiddleware` no longer mangles valueless or quoted HTML attributes.
- `SpaceLessMiddleware` no longer drops text after the final tag.
- `SpaceLessMiddleware` no longer corrupts non-UTF-8 HTML responses.
- `DatabaseRouter.allow_migrate` no longer blocks unmapped apps from migrating on the `default` database.

## [3.0.0] - 2026-06-25

### Added

- Add `csv` and `tsv` output formats to the `adminsitelog` management command.
- Add django-boost system checks for database router, redirect hostname
  middleware, user-agent optional dependency configuration, and logical
  deletion model configuration.
- Add `django_boost.template.StrictInvalidTemplateVariable` for raising an
  exception when Django renders invalid or missing template variables.
- Add a system check (`django_boost.W040`) that warns when the admin_tools app
  (`django_boost.contrib.admin_tools` or the deprecated
  `django_boost.admin_tools`) is in `INSTALLED_APPS` without
  `django.contrib.admin`.
- Add the correctly-spelled `django_boost.models.fields.ColorCodeField` model
  field (the canonical name for the previously misspelled `ColorCodeFiled`).

### Changed

- `adminsitelog` now writes the `delete complete` message to standard error
  for every output format (previously standard output in the default text
  format), so standard output carries only log data.
- Move the `admin_tools` app to `django_boost.contrib.admin_tools`. The old
  `django_boost.admin_tools` entry in `INSTALLED_APPS` still works but raises a
  `DeprecationWarning` and will be removed in django-boost 4.0.
- `listsuperuser` now reports audit fields (email, active, staff, last login)
  and supports `--format text|csv|tsv`, replacing its previous
  one-identifier-per-line output.
- Move the `adminsitelog` command into `django_boost.contrib.admin_tools`.
  Running it through `django_boost` alone still works but raises a
  `DeprecationWarning`; the core alias will be removed in django-boost 4.0.
- `adminsitelog` now exits with a clear error when `django.contrib.admin` is
  not in `INSTALLED_APPS`, instead of failing with an unrelated
  model-loading error.
- `adminsitelog` now reports an invalid `--filter`/`--exclude` operator or an
  unknown `--name_field` as a command error, instead of an unhandled traceback.
- Start the django-boost 3.0 development line by requiring Python 3.10+,
  dropping Django 3.x, and declaring support for Django 4.2-5.2 on
  officially supported Django/Python combinations.
- Use Django's native view setup and redirect mixin implementations now that
  django-boost requires Django 4.2+.
- Keep the `zip` template filter supported for backward compatibility and
  remove its v3 deprecation warning.
- Move user-agent detection behind the optional `useragent` extra. Core
  installs no longer include `user-agents`; install `django-boost[useragent]`
  before using `django_boost.context_processors.user_agent` or
  `UserAgentMixin`.
- `startapp_plus` now builds on Django's current app template, layering only
  the extra `forms.py` and `urls.py` on top, so generated apps inherit Django's
  defaults (such as `default_auto_field`). The previously bundled `apps.py`
  `ready()` stub and `views.py` generic-view imports are no longer added.
- Make logical deletion follow Django's deletion collector so `CASCADE`,
  `PROTECT`, `SET_NULL`, delete signals, queryset restrictions, and
  `(count, details)` delete return values are preserved.

### Deprecated

- Deprecate the misspelled `django_boost.models.fields.ColorCodeFiled` model
  field in favor of `ColorCodeField`; it now raises a `DeprecationWarning` and
  will be removed in django-boost 4.0.

### Removed

- Remove Django < 3.2 `default_app_config` shims and obsolete localization
  settings that are unnecessary for the Django 4.2+ baseline.
- Remove the deprecated `support_heroku` management command.
- Remove the deprecated `django_boost.models.fields.JsonField`.

### Fixed

- Fix `adminsitelog` user-name fallback for custom user models without a
  `username` attribute.
- Fix the `replace_parameters` template tag error message, which stated the
  argument count must be "odd" when it must be even.

## [2.2.0] - 2026-06-22

### Added

- Support passing `deleted_at` to logical deletion APIs so callers can set a
  custom deletion timestamp.

### Changed

- Document the planned django-boost 3.0 Python/Django baseline and
  `useragent` extra.

### Deprecated

- `zip` template filter. Use the `zip` template tag instead.
- `django_boost.models.fields.JsonField`. Use `django.db.models.JSONField`
  instead, available since Django 3.1.
- `support_heroku` management command. It will be removed in django-boost 3.0.

## [2.1.2] - 2026-06-21

### Fixed

- HTTP 510 reason phrase and add 511 in `STATUS_MESSAGES`.

## [2.1.1] - 2026-06-21

### Changed

- Declare support for Python 3.11 and 3.12.
- Declare support for Django 4.1 and 4.2.

### Fixed

- Restore compatibility with Python 3.8 and 3.9 by constraining the `ua-parser` dependency.

## [2.1.0] - 2022-09-08

### Changed

- Support Django 4.1.

## [2.0.0] - 2022-01-23

### Added

- `django_boost.views.simple.StringView`.
- `django_boost.admin_tools` sub app module.
- `listsuperuser` in `django_boost.admin_tools`.

### Changed

- Support Python 3.10.
- Support Django 4.0.

### Removed

- Support for Python 3.6 and 3.7.
- Support for Django 2.x.

## [1.7.2] - 2020-12-13

### Changed

- Regex pattern.
- Support Python 3.9.

## [1.7.1] - 2020-10-09

### Changed

- Some docstring updates.

### Fixed

- Internal JavaScript function does not work.

## [1.7] - 2020-09-24

### Added

- `revive` method to `django_boost.models.mixins.LogicalDeletionMixin`.
- `is_dead` method to `django_boost.models.mixins.LogicalDeletionMixin`.
- `is_alive` method to `django_boost.models.mixins.LogicalDeletionMixin`.

### Fixed

- `django_boost.utils.attribute.getattr_chain`.

## [1.6.2] - 2020-08-01

### Changed

- Some docstring updates.

## [1.6.1] - 2020-07-18

### Fixed

- Error in template `alive` filter.

## [1.6] - 2020-07-08

### Added

- `django_boost.models.mixins.LogicalDeletionMixin`.
- `django_boost.admin.LogicalDeletionModelAdmin`.
- `django_boost.validators.ContainAnyValidator`.

### Changed

- `django_boost.admin.sites.register_all` allows an options argument.

## [1.5.2] - 2020-05-23

### Changed

- Some translation updates.
- `support_heroku` command messages.

## [1.5.1] - 2020-04-19

### Changed

- Some translation updates.

## [1.5] - 2020-03-28

### Added

- `django_boost.middleware.SpaceLessMiddleware`.

## [1.4.2] - 2020-03-15

### Fixed

- Duplicated gunicorn entry in the `support_heroku` command.

## [1.4.1] - 2020-03-04

### Added

- `django_boost.forms.widgets.PhoneNumberInput`.
- `django_boost.forms.widgets.PhoneNumberField`.

## [1.4] - 2020-02-15

### Added

- `deletemigrations` command.
- `startapp_plus` command.
- Multiple database utility `DatabaseRouter`.

### Changed

- `ReAuthenticationRequiredMixin`.

### Removed

- `MuchedObjectGetMixin`.

## [1.3] - 2020-01-29

### Added

- Path converter `DateConverter` (`date`).
- `zip`, `zip_longest` and `chain` tags and `chunked` filter in `boost` template.
- `superuser` option in `StaffMemberRequiredMixin`.
- `--release` option in `support_heroku` command.

### Changed

- Support Django 3 and Python 3.8.
- `delattr` and `setattr` template tags return the argument value instead of `None`.

### Fixed

- A problem that some processes may be executed even when re-authentication is required.

## [1.2.3] - 2019-12-02

### Added

- `django_boost.forms.mixins.FieldRenameMixin`.

### Fixed

- Fixed an issue where `*.html` and `*.mo` were not included in the distribution package.

## [1.2.2] - 2019-11-10

### Added

- `django_boost.urls.include_static_files`.
- `django_boost.forms.fields.InvertBooleanField`.
- Template tag `var` in `boost`.
- Template tag `mimetype` in `mimetype`.
- Path converter keyword `float`.

### Removed

- Template tag `filter` in `boost`.

## [1.2.1] - 2019-10-30

### Changed

- New option `--name_field` to `adminsitelog` command.
- Supports cases where model has `ManyToManyField` (`RelatedModelInlineMixin`).

## [1.2] - 2019-10-17

### Added

- `support_heroku` command, which creates configuration files for Heroku.
- `AutoOneToOneField`.
- `RelatedModelInlineMixin`.
- New path converters `hex`, `oct`, `bin`, `hex_str`, `oct_str` and `bin_str`.
- New utility functions `getattrs`, `getattr_chain`, `hasattrs` and `hasattr_chain` in `utils.attribute`.
- New shortcut functions `get_object_or_default`, `get_object_or_exception`, `get_list_or_default` and `get_list_or_exception` in `shortcuts`.

### Changed

- Rename `MuchedObjectGetMixin` to `MatchedObjectGetMixin`.
- `MatchedObjectGetMixin` adds the `field_lookup` class variable to specify detailed search conditions.
- Multilingual support with automatic translation.

## [1.1.2] - 2019-10-02

### Added

- New template tag `literal`.
- `util.loop` function.
- `util.isiterable` function.

### Changed

- `HttpStatusCodeExceptions` DEBUG mode page design.

### Fixed

- `validators.validate_uuid4` and `validators.validate_json` errors.
- `context_processors.user_agent` and `views.mixins.UserAgentMixin` issue that could cause `KeyError`.

## [1.1.1] - 2019-09-23

### Added

- New template filter `filter`, `exclude` and `order_by` in `templatetags/boost_query`.

### Fixed

- `zip` filter does not work.

## [1.1] - 2019-09-10

### Added

- `UrlSet` class.
- `Http30X` class.
- `register_all` function.
- `adminsitelog` command.

### Changed

- `UUIDModelMixin` class `editable=False`.

## [1.0] - 2019-07-03

### Added

- First release.

[Unreleased]: https://github.com/ChanTsune/django-boost/compare/v3.3.1...HEAD
[3.3.1]: https://github.com/ChanTsune/django-boost/compare/v3.3.0...v3.3.1
[3.3.0]: https://github.com/ChanTsune/django-boost/compare/v3.2.4...v3.3.0
[3.2.4]: https://github.com/ChanTsune/django-boost/compare/v3.2.3...v3.2.4
[3.2.3]: https://github.com/ChanTsune/django-boost/compare/v3.2.2...v3.2.3
[3.2.2]: https://github.com/ChanTsune/django-boost/compare/v3.2.1...v3.2.2
[3.2.1]: https://github.com/ChanTsune/django-boost/compare/v3.2.0...v3.2.1
[3.2.0]: https://github.com/ChanTsune/django-boost/compare/v3.1.2...v3.2.0
[3.1.2]: https://github.com/ChanTsune/django-boost/compare/v3.1.1...v3.1.2
[3.1.1]: https://github.com/ChanTsune/django-boost/compare/v3.1.0...v3.1.1
[3.1.0]: https://github.com/ChanTsune/django-boost/compare/v3.0.1...v3.1.0
[3.0.1]: https://github.com/ChanTsune/django-boost/compare/v3.0.0...v3.0.1
[3.0.0]: https://github.com/ChanTsune/django-boost/compare/v2.2.0...v3.0.0
[2.2.0]: https://github.com/ChanTsune/django-boost/compare/v2.1.2...v2.2.0
[2.1.2]: https://github.com/ChanTsune/django-boost/compare/v2.1.1...v2.1.2
[2.1.1]: https://github.com/ChanTsune/django-boost/compare/v2.1.0...v2.1.1
[2.1.0]: https://github.com/ChanTsune/django-boost/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/ChanTsune/django-boost/compare/v1.7.2...v2.0.0
[1.7.2]: https://github.com/ChanTsune/django-boost/compare/v1.7.1...v1.7.2
[1.7.1]: https://github.com/ChanTsune/django-boost/compare/v1.7...v1.7.1
[1.7]: https://github.com/ChanTsune/django-boost/compare/v1.6.2...v1.7
[1.6.2]: https://github.com/ChanTsune/django-boost/compare/v1.6.1...v1.6.2
[1.6.1]: https://github.com/ChanTsune/django-boost/compare/v1.6...v1.6.1
[1.6]: https://github.com/ChanTsune/django-boost/compare/v1.5.2...v1.6
[1.5.2]: https://github.com/ChanTsune/django-boost/compare/v1.5.1...v1.5.2
[1.5.1]: https://github.com/ChanTsune/django-boost/compare/v1.5...v1.5.1
[1.5]: https://github.com/ChanTsune/django-boost/compare/v1.4.2...v1.5
[1.4.2]: https://github.com/ChanTsune/django-boost/compare/v1.4.1...v1.4.2
[1.4.1]: https://github.com/ChanTsune/django-boost/compare/v1.4...v1.4.1
[1.4]: https://github.com/ChanTsune/django-boost/compare/v1.3...v1.4
[1.3]: https://github.com/ChanTsune/django-boost/compare/v1.2.3...v1.3
[1.2.3]: https://github.com/ChanTsune/django-boost/compare/v1.2.2...v1.2.3
[1.2.2]: https://github.com/ChanTsune/django-boost/compare/v1.2.1...v1.2.2
[1.2.1]: https://github.com/ChanTsune/django-boost/compare/v1.2...v1.2.1
[1.2]: https://github.com/ChanTsune/django-boost/compare/v1.1.2...v1.2
[1.1.2]: https://github.com/ChanTsune/django-boost/compare/v1.1.1...v1.1.2
[1.1.1]: https://github.com/ChanTsune/django-boost/compare/v1.1...v1.1.1
[1.1]: https://github.com/ChanTsune/django-boost/compare/v1.0...v1.1
[1.0]: https://github.com/ChanTsune/django-boost/releases/tag/v1.0
