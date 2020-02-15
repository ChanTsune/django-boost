View Mixins
=========================

:synopsis: View mixin class in django-boost

Access Mixins
---------------

AllowContentTypeMixin
~~~~~~~~~~~~~~~~~~~~~~~

Restrict the content type of http request.

::

  from django.views.generic import TemplateView
  from django_boost.views.mixins import AllowContentTypeMixin

  class PostView(AllowContentTypeMixin, TemplateView):
      allowed_content_types = ["application/xml"]
      template_name = "path/to/template"


Restrict request based on ``Content-Type`` of http header.

If the content type is not allowed, http415 response will be returned.

You can disable restrictions by specifying ``strictly = False``


.. autoclass:: django_boost.views.mixins.ReAuthenticationRequiredMixin

LimitedTermMixin
~~~~~~~~~~~~~~~~~

::

  from datetime import datetime
  from django.views.generic import TemplateView
  from django_boost.views.mixins import LimitedTermMixin

  class LimitedTermMixin(LimitedTermMixin, TemplateView):
      template_name = 'path/to/template'
      start_datetime = datetime(year=2019, month=1, day=1)
      end_datetime = datetime(year=2019, month=12, day=31)

Restrict the period of access.  

``start_datetime`` specifies the date and time when access will be available, and ``end_datetime`` with the last date and time when access is available.

You can change the date and time that can be accessed dynamically by overriding the ``get_start_datetime`` and ``get_end_datetime`` methods, respectively.


You can specify the exception class to be thrown when the condition accessible to ``exception_class`` is not met.

The default is the ``Http404`` exception.

Redirect Control Mixins
------------------------

DynamicRedirectMixin
~~~~~~~~~~~~~~~~~~~~~

You can control the redirect destination with ``next=~~`` in the URL query string like ``LoginView``.

::

  from django.views,generic import FormView
  from django_boost.views.mixins import DynamicRedirectMixin

  class MyFormView(DynamicRedirectMixin, FormView):
      redirect_field_name = 'next' # default keyword is 'next'
      ...

You can change the query string parameter name by changing ``redirect_field_name``.

Adittional Attribute Mixins
----------------------------

UserAgentMixin
~~~~~~~~~~~~~~~

::

  from django_boost.views.generic import TemplateView
  from django_boost.views.mixins import UserAgentMixin

  class SameView(UserAgentMixin, TemplateView):
      template_name = "default_template"
      pc_template_name = "pc_template.html"
      tablet_template_name = "tablet_template.html"
      mobile_template_name = "mobile_template.html"

Assign ``user_agent`` attribute to ``self.request`` and switch the template file to be displayed by user agent.


If the user agent can not be determined, the template specified in ``template_name`` will be used.

``pc_template_name``, ``tablet_template_name``, ``mobile_template_name`` has no arms, but ``template_name`` is required.


JsonRequestMixin
~~~~~~~~~~~~~~~~~

A specialized mixin for ``AllowContentTypeMixin`` for json.

::

  from django.views.generic import TemplateView
  from django_boost.views.mixins import JsonRequestMixin

  class PostView(JsonRequestMixin, TemplateView):
      template_name = "path/to/template"

      def get_context_data(self,**kwargs):
          posted_data = self.json
          # {"send" : "from cliant"}
          return posted_data

You can access the dictionary object parsed from the Json string sent by the client in ``self.json``

If you use for the purpose of API, ``JsonView`` is recommended.

ResponseMixins
--------------

JsonResponseMixin
~~~~~~~~~~~~~~~~~

Returns the response in Json format

::

  from django.views.generic import TemplateView
  from django_boost.views.mixins import JsonResponseMixin

  class JsonResponseView(JsonResponseMixin, TemplateView):
      extra_context = {"context" : "..."}

      def get_context_data(self,**kwargs):
          context = {}
          context.update(super().get_context_data(**kwargs))
          return context

The usage of ``extra_context`` and ``get_context_data`` is basically the same as ``TemplateView``.

The difference is that ``TemplateView`` is passed directly to the template context, whereas ``JsonResponseMixin`` is a direct response.


Specify ``strictly = True`` if you want to limit the Content-Type to Json only.


If you use for the purpose of API ``JsonView`` below is recommended.

.. autoclass:: django_boost.views.mixins.SuperuserRequiredMixin

.. autoclass:: django_boost.views.mixins.StaffMemberRequiredMixin
