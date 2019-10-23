HttpStatusCode Exceptions
=========================

:synopsis: HttpStatusCode Exceptions like Http404 exception in django-boost


HttpStatusCode Exceptions
--------------------------

Provides exceptions for other status codes as well as Django's standard ``Http404`` exception.

::

  from django.http import JsonResponse
  from django_boost.http import Http400, Http415

  def view(request):
      if request.content_type != 'application/json':
          raise Http415
      return JsonResponse({"message":"ok"})


It is necessary to set :doc:`middleware` to use.

3XX
^^^^
::

  from django_boost.http import Http301

  ...
    raise Http301(redirect_url, message...)

Pass the redirect URL in the first argument.

Support ``Http301``, ``Http302``, ``Http307`` and ``Http308``.


4XX
^^^^

::

  from django_boost.http import Http415

  ...
    raise Http415(message...)

Support ``Http400``, ``Http401``, ``Http402``, ``Http403``, ``Http405``, ``Http406``, ``Http407``, ``Http408``, ``Http409``, ``Http410``,
``Http411``, ``Http412``, ``Http413``, ``Http414``, ``Http415``, ``Http416``, ``Http417``, ``Http418``,
``Http421``, ``Http422``, ``Http423``, ``Http424``, ``Http425``, ``Http426``, ``Http428``, ``Http429`` , ``Http431`` and ``Http451``.


5XX
^^^^

::

  from django_boost.http import Http500

  ...
    raise Http500(message...)

Support ``Http500``, ``Http501``, ``Http502``, ``Http503``, ``Http504`` and ``Http507``.
