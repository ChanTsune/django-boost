# Django-Boost  

Extension library to boost development with django

[![Downloads](https://pepy.tech/badge/django-boost)](https://pepy.tech/project/django-boost)

## Installation  

```
pip install django-boost
```

or

```
git clone https://github.com/ChanTsune/Django-Boost.git

python setup.py install
```

## Add an application  

settings.py
```py
INSTALLED_APPS = [
    ...
    'django_boost',
]
```

## use case  

### Custom User  

#### EmailUser  

settings.py
```py
...

AUTH_USER_MODEL = 'django_boost.EmailUser'

...
```
Replace Django default user model  
Use email address instead of username when logging in  

#### AbstractEmailUser  

```py
from django.db import models
from django_boost.models import AbstractEmailUser

class CustomUser(AbstractEmailUser):
    is_flozen = models.BoolField(default=False)
    homepage = models.URLField()

```
Available when you want to add a field to EmailUser  


### ModelMixins  

#### UUIDModelMixin  

```py
from django.db import models
from django_boost.models import UUIDModelMixin

class Stock(UUIDModelMixin):
    name = models.CharField(max_length=128)
    count = models.IntegerField()
```

Mixins that replace `id` from` AutoField` to `UUIDField`  

#### TimeStampModelMixin  

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

#### Combine  
```py
from django.db import models
from django_boost.models.mixins import UUIDMixin, TimeStampMixin

class Stock(UUIDModelMixin,TimeStampModelMixin):
    name = models.CharField(max_length=128)
    count = models.IntegerField()
```
Model mixins can also be combined in this way.  


### Fields  

#### ColorCodeField  
```py
from django.db import models
from django_boost.models.filed import ColorCodeField()

class Model(models.Model):
    color = ColorCodeField()

```
Save hexadecimal color code string including #.  
If you specify `upper=True`, the saved text will be capitalized.  
On the other hand, specifying `lower=True` will make the saved string lower case.  
You can not specify both at the same time.  
If neither is set, the string is saved without any changes.  
Default is `upper=False`,`lower=Flase`.  

### Middleware  

#### RedirectCorrectHostnameMiddleware

settings.py
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


#### HttpStatusCodeExceptionMiddleware  

settings.py
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

It is necessary to set `HttpStatusCodeExceptionMiddleware` to use


### Template context  

#### User Agent
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


### Access Mixins  

#### ReAuthenticationRequiredMixin  

```py
from django.views.generic import TemplateView
from django_boost.views.mixins import ReAuthenticationRequiredMixin

class RecentLogin(ReAuthenticationRequiredMixin,TemplateView):
    template_name = "mypage.html"
    auth_unnecessary = 3600
```

```py
from datetime import timedelta
from django.views.generic import TemplateView
from django_boost.views.mixins import ReAuthenticationRequiredMixin

class RecentLogin(ReAuthenticationRequiredMixin,TemplateView):
    template_name = "mypage.html"
    auth_unnecessary = timedelta(hours=1)
```


`auth_unnecessary` is the grace period until recertification.  
Can specify `int` and `timedelta` ,`None`.  
`None` is same as `0`.  

`logout=True`, Logout if the specified time limit has passed  
`logout=False`, Do not logout Even if the specified time limit has passed  

#### LimitedTermMixin  
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
`start_datetime` specifies the date and time when access will be available, and` end_datetime` with the last date and time when access is available.  

You can change the date and time that can be accessed dynamically by overriding the `get_start_datetime` and` get_end_datetime` methods, respectively.  

You can specify the exception class to be thrown when the condition accessible to `exception_class` is not met.  
The default is the `Http404` exception.  

### Redirect Control Mixins  

#### DynamicRedirectMixin  

You can control the redirect destination with `next=~` in the URL query string like `LoginView`.  

```py
from django.views,generic import FormView
from django_boost.views.mixins import DynamicRedirectMixin

class MyFormView(DynamicRedirectMixin, FormView):
    redirect_field_name = 'next' # default is 'next'
    ...
```

You can change the query string parameter name by changing `redirect_field_name`.  


### Adittional Attribute Mixins  

#### UserAgentMixin  
*Available only with Django 2.2 and higher*
```py
from django.views.generic import TemplateView
from django_boost.views.mixins import UserAgentMixin

class SameView(UserAgentMixin,TemplateView):
    pc_template_name = "pc_template.html"
    tablet_template_name = "tablet_template.html"
    mobile_template_name = "mobile_template.html"
```

Switch the template file to be displayed by user agent.  


### Form Mixin  

#### MuchedObjectGetMixin  
Object of the condition that matches the form input content.
Or mixin to add a method to get the query set.

```py
from django import forms
from django_boost.forms.mixins import MuchedObjectGetMixin
from .models import Customer

class CustomerForm(MuchedObjectGetMixin, forms.ModelForm):
    class Meta:
        models = Customer
        fields = ('name', )
```

```py
from django.views.generic import FormView
from .forms import CustomerForm

class CustomerSearchView(FormView):
    template_name = "form.html"
    form_class = CustomerForm

    def form_valid(self,form):
        object = form.get_object()  # get muched model object
        object_list = form.get_list()  # get muched models objects queryset

```

`MuchedObjectMixin` provides `get_object` and `get_list` methods, each of which returns a `model object` or `query set` that matches the form input content.  

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

###### Case of Namespaced  
`urls.py`  
```py
from django.urls import path, include
from . import views

app_name = "myapp"
urlpatterns = [
    path('views/',include(views.CustomerViews(app_name="myapp:customer").urls)),
]

```

In the template you can use as follows.  
```html+django
{% url 'myapp:customer:list' %}
{% url 'myapp:customer:create' %}
{% url 'myapp:customer:detail' %}
{% url 'myapp:customer:update' %}
{% url 'myapp:customer:delete' %}
```

### Template Tags  

Make Python built-in functions available in DjangoTemplate.  
Some non-built-in functions are also provided as filters. An example is `isiterable` filter.  
#### boost Filters  
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

#### boost_url Filters
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

#### boost_url Tags  

##### replace_parameters  
Replace the query string of the current page URL with the argument.  

```html+django
{% load boost_url %}

{# case of current page's query string is `?id=2`#}
{% replace_parameters request 'id' 1 'age' 20 %}

{# The result of replacing is `?id=1&age=20` #}

```
Useful for pagination.
