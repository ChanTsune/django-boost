from django.core.exceptions import (ImproperlyConfigured,
                                    MultipleObjectsReturned,
                                    ObjectDoesNotExist)
from django.forms import fields_for_model

from django_boost.utils.attribute import getattr_chain


class FormUserKwargsMixin:
    """Mixin to add `User model` to form instance variable."""

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)


class FieldRenameMixin:
    """
    ``FieldRenameMixin`` that changes form field names.

    Due to Python syntax, ``-`` cannot be included in form field names.

    Use it when the value of ``name`` attribute of
    HTML input element includes ``-`` due to restrictions of external library.

    ::

      from django import form
      from django_boost.forms.mixins import FieldRenameMixin

      class MyForm(FieldRenameMixin,forms.Form):
          token_id = forms.CharField()

          rename_field = {"token_id": "token-id"}

      MyForm().cleaned_data["token-id"]
    """

    rename_fields = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.rename_fields.items():
            if key != value:
                self.fields[value] = self.fields[key]
                del self.fields[key]


class MatchedObjectGetMixin:
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


class RelatedModelInlineMixin:
    """
    Mixin that treat two related `Model`'s as a single `Model`.

    example ::

    ```
    class ModelA(models.Model):
        text = models.TextField(...)


    class ModelB(models.Model):
        name = models.CharField(...)
        model_a = models.OneToOneField(to=ModelA, ...)
    ```

    ```
    class ModelBForm(RelatedModelInlineMixin, forms.ModelForm):
        inline_fields = {'model_a': ('text',)}

        class Meta:
            model = ModelB
            fields = ('name', )
    ```
    """

    inline_fields = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._related_field_model = {}
        for field, related_fields in self.inline_fields.items():
            model = self._meta.model
            try:  # reverse relation
                related_model = model._meta.fields_map[field].related_model
            except KeyError:  # forward relation
                related_model = getattr(model, field).field.related_model
            self._related_field_model.update({field: related_model})
            related_model_fields = fields_for_model(
                related_model, related_fields)

            for field_name, field_object in related_model_fields.items():
                if self.instance and self.instance.pk:
                    setattr(field_object, 'initial', getattr_chain(
                        self.instance, '%s.%s' % (field, field_name)))
                self.fields['%s_%s' % (field, field_name)] = field_object

    def save(self, commit=True):
        object = super().save(commit=False)
        for field, related_fields in self.inline_fields.items():
            related_model = self._related_field_model[field]
            rel_opts = related_model._meta
            pk_field_name = rel_opts.pk.attname
            rel_pk_field_name = '%s_%s' % (field, pk_field_name)
            if not hasattr(object, rel_pk_field_name):
                # case of reverse access
                if hasattr(object, field):
                    target_field = getattr(object, field)
                else:
                    name = None
                    for f in rel_opts.fields:
                        if f.related_model == type(object):
                            name = f.name
                            object.save()
                    target_field = related_model(**{name: object})
            elif getattr(object, rel_pk_field_name) is None:
                target_field = related_model()
            else:
                target_field = getattr(object, field)
            for related_field in related_fields:
                value = self.cleaned_data['%s_%s' % (field, related_field)]
                if self._is_many_to_many(rel_opts, related_field):
                    target_field.save()
                    getattr(target_field, related_field).set(value)
                else:
                    setattr(target_field, related_field, value)
            if commit:
                target_field.save()
            setattr(object, rel_pk_field_name, target_field.pk)
            setattr(object, field, target_field)
        if commit:
            object.save()
        return object

    def _is_many_to_many(self, rel_opts, field_name):
        for f in rel_opts.many_to_many:
            if f.attname == field_name:
                return True
        return False
