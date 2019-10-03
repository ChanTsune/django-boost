from django.core.exceptions import (ImproperlyConfigured,
                                    MultipleObjectsReturned,
                                    ObjectDoesNotExist)


class FormUserKwargsMixin:
    """Mixin to add `User model` to form instance variable."""

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)


class MuchedObjectGetMixin:
    """
    MatchedObjectGetMixin.

    This class adds methods that
    returns model object or queryset that matches the conditions.
    """

    model = None
    queryset = None
    raise_exception = False
    field_lookup = {}

    def get_queryset(self):
        if self.queryset is None:
            if self.model:
                return self.model._default_manager.all()
            elif hasattr(self, '_meta') and self._meta.model:
                return self._meta.model._default_manager.all()
            else:
                raise ImproperlyConfigured(
                    "%(cls)s is missing a QuerySet. Define "
                    "%(cls)s.model, %(cls)s.queryset, or override "
                    "%(cls)s.get_queryset()." % {
                        'cls': self.__class__.__name__
                    }
                )
        self.model_class = self.queryset.model
        return self.queryset.all()

    def _replace_fields(self, form_data):
        filter_data = {}
        for k, v in form_data.items():
            filter_data[self.field_lookup.get(k, k)] = v
        return filter_data

    def get_list(self, queryset=None):
        """Return matched object queryset."""
        if queryset is None:
            queryset = self.get_queryset()
        filter_data = self._replace_fields(self.cleaned_data)
        return queryset.filter(**filter_data)

    def get_object(self, queryset=None):
        """Return matched object."""
        try:
            return self.get_list(queryset).get()
        except (MultipleObjectsReturned, ObjectDoesNotExist) as e:
            if self.raise_exception:
                raise e
            return None
