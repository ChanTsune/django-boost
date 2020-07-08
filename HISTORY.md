# HISTORY  

## Versions  

### 1.6
- Add
  - `django_boost.models.mixins.LogicalDeletionMixin`
  - `django_boost.admin.LogicalDeletionModelAdmin`
  - `django_boost.validators.ContainAnyValidator`
- Update
  - `django_boost.admin.sites.register_all` allow options argument.

### 1.5.2
- Update
  - some translation updates
  - `support_heroku` command messages

### 1.5.1

- Update
  - some translation updates

### 1.5  

- Add
  - `django_boost.middleware.SpaceLessMiddleware`

### 1.4.2  

- Fix
  - on support_heroku command duplicated gunicorn

### 1.4.1  

- Add
  - `django_boost.forms.widgets.PhoneNumberInput`
  - `django_boost.forms.widgets.PhoneNumberField`

### 1.4  

- Add
  - `deletemigrations` command
  - `startapp_plus` command
  - multiple database util `DatabaseRouter`
- Update
  - `ReAuthenticationRequiredMixin`
- Delete
  - `MuchedObjectGetMixin`

### 1.3  

- Add
  - path converter `DateConverter` (`date`)
  - `zip`, `zip_longest` and `chain` tags and `chunked` filter in `boost` template

- Update  
  - add `superuser` option in `StaffMemberRequiredMixin`  
  - support Django3 and python3.8
  - add option `--release` in `support_heroku` command

- Change  
  - `delattr` and `setattr` template tags return value `None` to argument value

- Fix  
  - A problem that some processes may be executed even when re-authentication is required

### 1.2.3  

- Add  
  - `django_boost.forms.mixins.FieldRenameMixin`  
- Fix  
  - Fixed an issue where `*.html` and `*.mo` were not included in the distribution package

### 1.2.2  

- Add  
  - `django_boost.urls.include_static_files`  
  - `django_boost.forms.fields.InvertBooleanField`  
  - Template tag `var` in boost  
  - Template tag `mimetype` in mimetype  
  - Path converter keyword `float`  
- Delete  
  - Template tag `filter` in boost

### 1.2.1  

- Update  
  - new option `--name_field` to `adminsitelog` command.  
  - Supports cases where model has `ManyToManyField`(`RelatedModelInlineMixin`).  

### 1.2  

- Add  
  - `support_heroku` command, Create a configuration file for heroku  
  - `AutoOneToOneField`  
  - `RelatedModelInlineMixin`  
  - new Path Converters `hex`,`oct`,`bin`,`hex_str`,`oct_str` and `bin_str`  
  - new utility functions `getattrs`,`getattr_chain`,`hasattrs` and `hasattr_chain` in `utils.attribute`  
  - new shortcut functions `get_object_or_default`,`get_object_or_exception`, `get_list_or_default`,`get_list_or_exception` in `shortcuts`  
- Change  
  - rename `MuchedObjectGetMixin` to `MatchedObjectGetMixin`  
- Update  
  - `MatchedObjectGetMixin` Add `field_lookup` class variable to specify detailed search conditions  
  - Multilingual support with automatic translation  

### 1.1.2  

- Add  
  - new template tag `literal`  
  - `util.loop` function  
  - `util.isiterable` function  
- Update  
  - `HttpStatusCodeExceptions` DEBUG mode page design  
- Fix  
  - `validators.validate_uuid4`,`validators.validate_json` error  
  - `context_processors.user_agent`,`views.mixins.UserAgentMixin` issue that could cause `KeyError`  

### 1.1.1  

- Add  
  - new template filter `filter`,`exclude`,`order_by` in `templatetags/boost_query`
- Fix  
  - `zip` filter doesn't work

### 1.1  

- Add  
  - UrlSet class  
  - Http30X class  
  - register_all function  
  - adminsitelog Command  
- Change  
  - UUIDModelMixin class `editable=False`  

### 1.0  

- First release  
