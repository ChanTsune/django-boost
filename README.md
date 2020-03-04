# Django-Boost  

Django Boost is a collection of custom extensions for the Django Framework.  

[![PyPI - License](https://img.shields.io/pypi/l/django_boost)](https://pypi.org/project/django-boost/)
[![Build Status](https://travis-ci.org/ChanTsune/django-boost.svg?branch=master)](https://travis-ci.org/ChanTsune/django-boost)
[![PyPI](https://img.shields.io/pypi/v/django_boost)](https://pypi.org/project/django-boost/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/django_boost)](https://pypi.org/project/django-boost/)
[![Downloads](https://pepy.tech/badge/django-boost)](https://pepy.tech/project/django-boost)

## Documentation  

You can view documentation online at:

[https://django-boost.readthedocs.io/en/latest/](https://django-boost.readthedocs.io/en/latest/)

Or you can look at the docs/ directory in the repository.

## Getting It

```bash
pip install django-boost
```

or

```bash
git clone https://github.com/ChanTsune/Django-Boost.git

python setup.py install
```

## Installing It

To enable django_boost in your project you need to add it to INSTALLED_APPS in your projects settings.py file:

```py
INSTALLED_APPS = [
    ...
    'django_boost',
    ...
]
```

## Brief introduction  

### EmailUser  

`settings.py`

```py
AUTH_USER_MODEL = 'django_boost.EmailUser'
```

Replace Django default user model  
Use email address instead of username when logging in  

### AbstractEmailUser  

```py
from django.db import models
from django_boost.models import AbstractEmailUser

class CustomUser(AbstractEmailUser):
    is_flozen = models.BoolField(default=False)
    homepage = models.URLField()

```

Available when you want to add a field to EmailUser  

### UUIDModelMixin  

```py
from django.db import models
from django_boost.models import UUIDModelMixin

class Stock(UUIDModelMixin):
    name = models.CharField(max_length=128)
    count = models.IntegerField()
```

Mixins that replace `id` from `AutoField` to `UUIDField`  

### TimeStampModelMixin  

```py
from django.db import models
from django_boost.models.mixins import TimeStampModelMixin

class Stock(TimeStampModelMixin):
    name = models.CharField(max_length=128)
    count = models.IntegerField()
```

The fields `posted_at` and `updated_at` are added.  

```py
posted_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
```

### ColorCodeField  

```py
from django.db import models
from django_boost.models.fields import ColorCodeField

class MyModel(models.Model):
    color = ColorCodeField()

```

Save hexadecimal color code string including #.  
If you specify `upper=True`, the saved text will be capitalized.  
On the other hand, specifying `lower=True` will make the saved string lower case.  
You can not specify both at the same time.  
If neither is set, the string is saved without any changes.  
Default is `upper=False`,`lower=Flase`.  

### SplitDateTimeField  

```py
from django.db import models
from django_boost.models.fields import SplitDateTimeField

class MyModel(models.Model):
    date = SplitDateTimeField()
```

A little convenient DateTimeField.

`SplitDateTimeField` is the form_class of `django.models.db.DateTimeField` replaced with `django.forms.SplitDateTimeField`.

Internal DB field is the same as `django.models.db.DateTimeField`.

### AutoOneToOneField  

```py
from django.db import models
from django_boost.models.fields import AutoOneToOneField

class UserProfile(models.Model):
    user = AutoOneToOneField(User, primary_key=True, related_name='profile')
    home_page = models.URLField(max_length=255, blank=True)
```

### RedirectCorrectHostnameMiddleware

`settings.py`

```py

MIDDLEWARE = [
    'django_boost.middleware.RedirectCorrectHostnameMiddleware',  # django_boost
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    ...
]

...

CORRECT_HOST = 'sample.com'

```

Redirect all access to the domain specified in `CORRECT_HOST`

It is not redirected when `DEBUG = True`  

This is useful when migrating domains  

Originally it should be done with server software such as nginx and apache, but it is useful when the setting is troublesome or when using services such as heroku  

### HttpStatusCodeExceptionMiddleware  

`settings.py`

```py
MIDDLEWARE = [
    'django_boost.middleware.HttpStatusCodeExceptionMiddleware',  # django_boost
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    ...
]
```

It is necessary to use the `HttpStatusCode exceptions` described later.

### HttpStatusCode Exceptions  

Provides exceptions for other status codes as well as Django's standard `Http404` exception  

```py
from django.http import JsonResponse
from django_boost.http import Http400, Http415

def view(request):
    if request.content_type != 'application/json':
        raise Http415
    return JsonResponse({"message":"ok"})

```

This Middleware is required when using `HttpStatusCodeExceptionMiddleware`  

### User Agent in Template context

```py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_boost.context_processors.user_agent', # django boost
            ],
        },
    },
]
```

When given a user agent like `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36`, provide the following context to the template  

```py
{'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
'browser': 'Chrome',
'device': 'Other',
'is_bot': False,
'is_email_client': False,
'is_mobile': False,
'is_pc': True,
'is_tablet': False,
'is_touch_capable': False,
'os': 'Mac OS X'}
```

These information is obtained using [user-agents](https://github.com/selwin/python-user-agents)  

### AllowContentTypeMixin  

Restrict the content type of http request.  

```py
from django.views.generic import TemplateView
from django_boost.views.mixins import AllowContentTypeMixin

class PostView(AllowContentTypeMixin, TemplateView):
    allowed_content_types = ["application/xml"]
    template_name = "path/to/template"

```

Restrict request based on `Content-Type` of http header.  

If the content type is not allowed, http415 response will be returned.  
You can disable restrictions by specifying `strictly = False`  

### LimitedTermMixin  

```py
from datetime import datetime
from django.views.generic import TemplateView
from django_boost.views.mixins import LimitedTermMixin

class LimitedTermMixin(LimitedTermMixin, TemplateView):
    template_name = ''
    start_datetime = datetime(year=2019, month=1, day=1)
    end_datetime = datetime(year=2019, month=12, day=31)

```

Restrict the period of access.  
`start_datetime` specifies the date and time when access will be available, and `end_datetime` with the last date and time when access is available.  

You can change the date and time that can be accessed dynamically by overriding the `get_start_datetime` and `get_end_datetime` methods, respectively.  

You can specify the exception class to be thrown when the condition accessible to `exception_class` is not met.  
The default is the `Http404` exception.  

### DynamicRedirectMixin  

You can control the redirect destination with `next=~` in the URL query string like `LoginView`.  

```py
from django.views,generic import FormView
from django_boost.views.mixins import DynamicRedirectMixin

class MyFormView(DynamicRedirectMixin, FormView):
    redirect_field_name = 'next' # default is 'next'
    ...
```

You can change the query string parameter name by changing `redirect_field_name`.  

### UserAgentMixin  

```py
from django_boost.views.generic import TemplateView
from django_boost.views.mixins import UserAgentMixin

class SameView(UserAgentMixin, TemplateView):
    template_name = "default_template"
    pc_template_name = "pc_template.html"
    tablet_template_name = "tablet_template.html"
    mobile_template_name = "mobile_template.html"
```

Assign `user_agent` attribute to `self.request` and switch the template file to be displayed by user agent.  

If the user agent can not be determined, the template specified in `template_name` will be used.  
`pc_template_name`,`tablet_template_name`,`mobile_template_name` has no arms, but `template_name` is required.  

### JsonRequestMixin  

A specialized mixin for `AllowContentTypeMixin` for json.  

```py
from django.views.generic import TemplateView
from django_boost.views.mixins import JsonRequestMixin

class PostView(JsonRequestMixin, TemplateView):
    template_name = "path/to/template"

    def get_context_data(self,**kwargs):
        posted_data = self.json
        # {"send" : "from cliant"}
        return posted_data
```

You can access the dictionary object parsed from the Json string sent by the client in `self.json`  

If you use for the purpose of API `JsonView` below is recommended.  

### JsonResponseMixin  

Returns the response in Json format  

```py
from django.views.generic import TemplateView
from django_boost.views.mixins import JsonResponseMixin

class JsonResponseView(JsonResponseMixin, TemplateView):
    extra_context = {"context" : "..."}

    def get_context_data(self,**kwargs):
        context = {}
        context.update(super().get_context_data(**kwargs))
        return context

```

The usage of `extra_context` and `get_context_data` is basically the same as `TemplateView`.
The difference is that `TemplateView` is passed directly to the template context, whereas `JsonResponseMixin` is a direct response.  

Specify `strictly = True` if you want to limit the Content-Type to Json only.  

If you use for the purpose of API `JsonView` below is recommended.  

### MatchedObjectGetMixin  

Object of the condition that matches the form input content.
Or mixin to add a method to get the queryset.

```py
from django import forms
from django_boost.forms.mixins import MatchedObjectGetMixin
from .models import Customer

class CustomerForm(MatchedObjectGetMixin, forms.ModelForm):
    class Meta:
        models = Customer
        fields = ('name', )
        field_lookup = {'name' : 'name__startswith'} # filter lookup kwargs
```

Set `field_lookup` to set detailed search conditions.  

```py
from django.views.generic import FormView
from .forms import CustomerForm

class CustomerSearchView(FormView):
    template_name = "form.html"
    form_class = CustomerForm

    def form_valid(self,form):
        object = form.get_object()  # get matched model object
        object_list = form.get_list()  # get matched models objects queryset

```

`MatchedObjectMixin` provides `get_object` and `get_list` methods, each of which returns a `model object` or `queryset` that matches the form input content.  

### RelatedModelInlineMixin  

Mixin that treat two related `Model`'s as a single `Model`.

```py
class ModelA(models.Model):
    text = models.TextField(...)


class ModelB(models.Model):
    name = models.CharField(...)
    model_a = models.OneToOneField(to=ModelA, ...)
```

```py
class ModelBForm(RelatedModelInlineMixin, forms.ModelForm):
    inline_fields = {'model_a': ('text',)}

    class Meta:
        model = ModelB
        fields = ('name', )
```

### GenericView  

#### Extended Views  

```py
from django_boost.views.generic import View

class YourView(View):

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        ## some process before view process

        ## For example, add attribute to view class

    def after_view_process(self, request, response, *args, **kwargs):
        super().after_view_process(request, response, *args, **kwargs)
        ## some process after view process

        ## For example, add http headers to the response

        return response

```

django_boost generic view (
`CreateView`, `DeleteView`, `DetailView`, `FormView`, `ListView`, `TemplateView`, `UpdateView`, `View`) classes has `setup` and `after_view_process` method, These are called before and after processing of View respectively. `setup` method is same as the method added in Django 2.2 .

#### JsonView  

A generic view class that inherits `JsonResponseMixin` and `JsonRequestMixin`.  

```py
from django_boost.views.generic import JsonView

class SameAPIView(JsonView):

    def get_context_data(self,**kwargs):
        return self.json
```

In the above example, we just return the sent Json string as it is.  

#### ModelCRUDViews  

Provides easy creation of CRUDViews linked to model.  

`views.py`  

```py
from django_boost.views.generic import ModelCRUDViews

class CustomerViews(ModelCRUDViews):
    model = Customer
```

`urls.py`  

```py
from django.urls import path, include
from . import views

urlpatterns = [
    path('views/',include(views.CustomerViews().urls)),
]
```

In the template you can use as follows.  

```html+django
{% url 'customer:list' %}
{% url 'customer:create' %}
{% url 'customer:detail' %}
{% url 'customer:update' %}
{% url 'customer:delete' %}
```

The name of the URL is defined under the namespace of the lower-cased model class name.  

### Path Converters  

```py
from django_boost.urls import register_boost_converters

register_boost_converters()
```

Add `hex`, `oct`, `bin`, `hex_str`,`oct_str`and `bin_str` to path converter keyword.  

```py
from django.urls import path
from django_boost.urls import register_boost_converters

register_boost_converters()

urlpatterns = [
    path('bin/<bin:id>', ~~),
    path('oct/<bin:id>', ~~),
    path('hex/<bin:id>', ~~),
]
```

`bin` match `[01]+`,`oct` match `[0-7]+`, `hex` match `[0-9a-fA-F]`  
These are passed as `int` type to the python program.  

Keywords that end with `_str` are passed as `str` type to python program.  

### Shortcut Functions  

```py
from django_boost.shortcuts import (
    get_list_or_default, get_list_or_exception,
    get_object_or_default, get_object_or_exception)

my_model = MyModel.objects.get(id=1)
get_object_or_default(MyModel, default=my_model, id=2)

get_object_or_exception(MyModel, exception=Exception, id=2)

```

These behave like `get_object_or_404`  

### UrlSet  

If URLs corresponding to multiple models are described in one `urls.py`, it may be redundant.  
As below.  

```python
from django.urls import path

from . import views

urlpatterns = [
    path('modelA/', views.ModelAListView.as_view(), name='modelA_list'),
    path('modelA/create/', views.ModelACreateView.as_view(), name='modelA_create'),
    path('modelA/<int:pk>/', views.ModelADetailView.as_view(), name='modelA_detail'),
    path('modelA/<int:pk>/update/', views.ModelAUpdateView.as_view(), name='modelA_update'),
    path('modelA/<int:pk>/delete/', views.ModelADeleteView.as_view(), name='modelA_delete'),
    path('modelB/', views.ModelBListView.as_view(), name='modelB_list'),
    path('modelB/create/', views.ModelBCreateView.as_view(), name='modelB_create'),
    path('modelB/<int:pk>/', views.ModelBDetailView.as_view(), name='modelB_detail'),
    path('modelB/<int:pk>/update/', views.ModelBUpdateView.as_view(), name='modelB_update'),
    path('modelB/<int:pk>/delete/', views.ModelBDeleteView.as_view(), name='modelB_delete'),
]
```

Originally it would be desirable to split the file, but doing so can lead to poor code outlook, due to the increase in files.  

In such cases, you can use `UrlSet`.

When the above code is rewritten using `UrlSet`, it becomes as follows.  

```python
from django.urls import path, include
from django_boost.urls import UrlSet

from . import views

class ModelAUrlSet(UrlSet):
    app_name = "ModelA"
    urlpatterns = [
        path('', views.ModelAListView.as_view(), name='list'),
        path('create/', views.ModelACreateView.as_view(), name='create'),
        path('<int:pk>/', views.ModelADetailView.as_view(), name='detail'),
        path('<int:pk>/update/', views.ModelAUpdateView.as_view(), name='update'),
        path('<int:pk>/delete/', views.ModelADeleteView.as_view(), name='delete'),
    ]

class ModelBUrlSet(UrlSet):
    app_name = "ModelB"
    urlpatterns = [
        path('', views.ModelBListView.as_view(), name='list'),
        path('create/', views.ModelBCreateView.as_view(), name='create'),
        path('<int:pk>/', views.ModelBDetailView.as_view(), name='detail'),
        path('<int:pk>/update/', views.ModelBUpdateView.as_view(), name='update'),
        path('<int:pk>/delete/', views.ModelBDeleteView.as_view(), name='delete'),
    ]

urlpatterns = [
    path('modelA/', include(ModelAUrlSet)),
    path('modelB/', include(ModelBUrlSet)),
]
```

URLs are grouped for easy reading.  

### Admin Site Utilitys  

Easily register Models to Django admin site.  

```py
from your_app import models
from django_boost.admin.sites import register_all

register_all(models)
```

Register all models defined in `models.py` in Django admin site.  

Custom admin classes are also available.  

```py
from your_app import models
from your_app import admin
from django_boost.admin.sites import register_all

register_all(models, admin_class=admin.CustomAdmin)
```

### Template Tags  

Make Python built-in functions available in DjangoTemplate.  
Some non-built-in functions are also provided as filters. An example is `isiterable` filter.  

#### Load filters  

```html+django
{% load boost %}
```

##### isiterable  

isiterable filter returns True if it filters repeatable objects, and False otherwise.  

```html+django
{% load boost %}

{% if object|isiterable %}
  {% for i in object %}
    <p>{{ i }}</p>
  {% endfor %}
{% else %}
  <p>{{ object }}</p>
{% endif %}

```

#### literal  

Python literal from string.  
Using backend `ast.literal_eval`.  

```html+django
{% load boost %}

{% literal "[1, 2, 3]" as list %}

{% for i in list %}
    <p>{{ i }}</p>
{% endfor %}
```

#### URL Utility  

```html+django
{% load boost_url %}
```

##### urlencode  

URL encode the filtered string.  
You can specify non-conversion characters in the argument.  

```html+django
{% load boost_url %}

{{ url | urlencode }}

{{ url | urlencode:'abc' }}

```

##### urldecode  

The reverse of `urlencode`.  

```html+django
{% load boost_url %}

{{ url | urldecode }}
```

##### replace_parameters  

Replace the query string of the current page URL with the argument.  

```html+django
{% load boost_url %}

{# case of current page's query string is `?id=2`#}
{% replace_parameters request 'id' 1 'age' 20 %}

{# The result of replacing is `?id=1&age=20` #}

```

Useful for pagination.  

#### Queryset Utility  

```html+django
{% load boost_query %}
```

Make the query set methods available in the template.

`filter`, `exclude`, `order_by` are available.

If you use the LogicalDeletionMixin, you can also use `alive` and `dead`  

```html+django
{% qureyset|filter:"field=value"%}

{% qureyset|exclude:"field=value"%}

{% qureyset|order_by:"field"%}

{# If it inherits LogicalDeletionMixin. #}

{% qureyset|alive %}

{% qureyset|dead %}

```

## utilty functions  

### loop utils  

#### Django Template like forloop  

```py
from django_boost.utils import loop

for forloop, item in loop([1, 2, 3, 4, 5]):
    forloop.counter0
    forloop.counter
    forloop.revcounter0
    forloop.revcounter
    forloop.first
    forloop.last
```

Provides Django Template loops to Python programs.  

#### loopfirst  

Yield True when the first element of the given iterator object, False otherwise.  

```py
from django_boost.utils.functions import loopfirst


for is_first, v in loopfirst(range(5)):
    print(is_first, v)

# True 0
# False 1
# False 2
# False 3
# False 4
```

#### looplast  

Yield True when the last element of the given iterator object, False otherwise.  

```py
from django_boost.utils.functions import looplast


for is_last, v in looplast(range(5)):
    print(is_last, v)

# False 0
# False 1
# False 2
# False 3
# True 4
```

#### loopfirstlast  

A function combining `firstloop` and `lastloop`.  

Yield True if the first and last element of the iterator object, False otherwise.  

```py
from django_boost.utils.functions import loopfirstlast


for first_or_last, v in loopfirstlast(range(5)):
    print(first_or_last, v)

# True 0
# False 1
# False 2
# False 3
# True 4
```

### Commands  

#### adminsitelog  

```bash
python manage.py adminsitelog
```

View and delete Admin Site logs.  

##### view all logs  

```bash
python manage.py adminsitelog
```

```bash
id| action | detail | user | time
6 | Deleted | Customer object (8) | admin | 2019-08-19 14:56:29.609940+00:00
7 | Added | Customer object (11) | admin | 2019-08-20 16:12:38.902129+00:00
8 | Changed | Customer object (4) - Changed color. | admin | 2019-08-20 16:12:45.653693+00:00
```

##### filter logs  

```bash
python manage.py adminsitelog --filter "action_time>=2019-8-01" --exclude "id=6"
```

```bash
id | action | detail | user | time
7 | Added | Customer object (11) | admin | 2019-08-20 16:12:38.902129+00:00
8 | Changed | Customer object (4) - Changed color. | admin | 2019-08-20 16:12:45.653693+00:00
```

##### delete all logs  

```bash
python manage.py adminsitelog --delete
```

It is also possible to delete only the logs narrowed down by `--filter` and `--exclude`.  

#### support_heroku  

```bash
python manage.py support_heroku
```

Create heroku config files.  
`Procfile`,`runtime.txt`,`requirements.txt`  

For more details.  

```bash
python manage.py support_heroku -h
```
