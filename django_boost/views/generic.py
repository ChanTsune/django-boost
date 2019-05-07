from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.utils.translation import gettext as _
from django.views.generic import View

from django_boost.utils.functions import model_to_json
from django_boost.views.mixins import JsonRequestMixin, JsonResponseMixin


class SingleObjectMixin:

    model = None
    queryset = None
    fields = ()
    exclude = ()
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    query_pk_and_slug = False

    def get_object(self, queryset=None):
        """
        Return the object requested by the view.

        Require `self.queryset` and a `pk` or `slug` argument in the URLconf.
        Subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def get_queryset(self):
        """
        Return the `QuerySet` that will be used to look up the object.

        This method is called by the default implementation of get_object() and
        may not be called if get_object() is overridden.
        """
        if self.queryset is None:
            if self.model:
                return self.model._default_manager.all()
            else:
                raise ImproperlyConfigured(
                    "%(cls)s is missing a QuerySet. Define "
                    "%(cls)s.model, %(cls)s.queryset, or override "
                    "%(cls)s.get_queryset()." % {
                        'cls': self.__class__.__name__
                    }
                )
        return self.queryset.all()

    def get_slug_field(self):
        """Get the name of a slug field to be used to look up by slug."""
        return self.slug_field

    def get_fields(self):
        return self.fields

    def get_exclude(self):
        return self.exclude

    def object_to_json(self):
        fields = self.get_fields()
        exclude = self.get_exclude()
        if hasattr(self.object, 'to_json'):
            return self.object.to_json(fields, exclude)
        return model_to_json(self.object, fields, exclude)

    def get_response_data(self, **kwargs):
        """Insert the single object into the dict."""
        return super().get_response_data(**self.object_to_json())


class JsonView(JsonRequestMixin, JsonResponseMixin, View):
    """Return JsonResponse view."""


class JsonDitailView(SingleObjectMixin, JsonView):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)


class JsonCreateView(JsonView):
    pass


class JsonUpdateView(JsonView):
    pass


class JsonDeleteView(JsonView):
    pass
