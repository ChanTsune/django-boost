Template Tags
==============

:synopsis: Template Tags in django-boost


Python built-in functions
--------------------------

Make Python built-in functions available in DjangoTemplate.

Some non-built-in functions are also provided as filters.
A live example of the most useful helpers is available in the sample app at the home page.

The sample page demonstrates helpers such as ``abs``, ``len``, ``iter``, ``next``, ``chunked``, ``literal``, and ``zip`` so the available tags and filters are easy to discover from a running project.

Usage
~~~~~~~~~~~~

::

  {% load boost %}

isiterable
~~~~~~~~~~~

``isiterable`` filter returns True if it filters repeatable objects, and False otherwise.

::

  {% load boost %}

  {% if object|isiterable %}
    {% for i in object %}
      <p>{{ i }}</p>
    {% endfor %}
  {% else %}
    <p>{{ object }}</p>
  {% endif %}


literal
~~~~~~~~

Python literal from string.
Using backend ``ast.literal_eval``.

::

  {% load boost %}

  {% literal "[1, 2, 3]" as list %}

  {% for i in list %}
      <p>{{ i }}</p>
  {% endfor %}

chain
~~~~~~~~
Concatenate iterable objects

::

  {% load boost %}

  {% chain list1 list2 as concatenated_list %}

  {% for i in concatenated_list %}
    {{ i }}
  {% endfor %}


chunked
~~~~~~~~
Break *iterable* into lists of length *n*

::

  {% load boost %}

  {% for i in list|chunked:3 %}
    {% for j in i %}
      {{ j }}
    {% endfor %}
  {% endfor %}

zip
~~~~
Combine iterable objects.

Use the ``zip`` template filter when combining two iterables inline. If you
need to combine three or more iterables at the same time, use the ``zip``
template tag instead.

::

  {% load boost %}

  {% for value1, value2 in list1|zip:list2 %}
    {{ value1 }} {{ value2 }}
  {% endfor %}

  {% zip list1 list2 list3 as zipped_list %}

  {% for value1, value2, value3 in zipped_list %}
    {{ value1 }} {{ value2 }} {{ value3 }}
  {% endfor %}


URL Utility
------------

Usage
~~~~~~~~~~~~

::

  {% load boost_url %}

urlencode
~~~~~~~~~~

URL encode the filtered string.
You can specify non-conversion characters in the argument.

::

  {% load boost_url %}

  {{ url | urlencode }}

  {{ url | urlencode:'abc' }}

.. note::

   Django ships an equivalent built-in ``urlencode`` filter (its argument is
   named ``safe``), so prefer the built-in when you only need URL encoding.
   This filter is kept mainly to pair with ``urldecode`` below, for which
   Django has no built-in.


urldecode
~~~~~~~~~~

The reverse of ``urlencode``.

::

  {% load boost_url %}

  {{ url | urldecode }}

replace_parameters
~~~~~~~~~~~~~~~~~~~

Replace the query string of the current page URL with the argument.

::

  {% load boost_url %}

  {# case of current page's query string is `?id=2`#}
  {% replace_parameters request 'id' 1 'age' 20 %}

  {# The result of replacing is `?id=1&age=20` #}

Useful for pagination.

get_querystring
~~~~~~~~~~~~~~~~

return querystring value

::

  {% load boost_url %}

  {% get_querystring request 'id' %}

  {# return request.GET.get('id', None) #}


Queryset Utility
-----------------

Usage
~~~~~~~~~~~~

::

  {% load boost_query %}

Make the query set methods available in the template.

``filter``, ``exclude``, ``order_by`` are available.

If you use the LogicalDeletionMixin, you can also use ``alive`` and ``dead``

::

  {% for obj in queryset|filter:"field=value" %}...{% endfor %}

  {% for obj in queryset|exclude:"field=value" %}...{% endfor %}

  {% for obj in queryset|order_by:"field" %}...{% endfor %}

  {# If it inherits LogicalDeletionMixin. #}

  {% for obj in queryset|alive %}...{% endfor %}

  {% for obj in queryset|dead %}...{% endfor %}


MimeType Utility
-----------------

Usage
~~~~~~~~~~~~

::

  {% load mimetype %}

mimetype
~~~~~~~~~

Guess mimetype from the extension at the end of the string.

Python ``mimetypes.guess_type`` is used internally.

::

  {{ "json"|mimetype }} {# "application/json" #}

  {{ ".json"|mimetype }} {# "application/json" #}

  {{ "sample.json"|mimetype }} {# "application/json" #}
