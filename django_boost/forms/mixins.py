"""Form mixins for Django's ``django.forms``."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, ClassVar, TYPE_CHECKING, cast

from django import forms
from django.core.exceptions import (ImproperlyConfigured,
                                    MultipleObjectsReturned,
                                    ObjectDoesNotExist)
from django.db.models import Model, QuerySet
from django.forms import fields_for_model

from django_boost.utils.attribute import getattr_chain

if TYPE_CHECKING:
    _FormHost = forms.Form
    _ModelFormHost = forms.ModelForm
else:
    _FormHost = object
    _ModelFormHost = object


class FormUserKwargsMixin(_FormHost):
    """Mixin that pulls a ``user`` keyword argument into ``self.user``."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Pop the ``user`` keyword argument into ``self.user`` before delegating to the form."""
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)


class FieldRenameMixin(_FormHost):
    """
    ``FieldRenameMixin`` that changes form field names.

    Due to Python syntax, ``-`` cannot be included in form field names.

    Use it when the value of ``name`` attribute of
    HTML input element includes ``-`` due to restrictions of external library.

    ::

      from django import forms
      from django_boost.forms.mixins import FieldRenameMixin

      class MyForm(FieldRenameMixin,forms.Form):
          token_id = forms.CharField()

          rename_fields = {"token_id": "token-id"}

      MyForm().cleaned_data["token-id"]
    """

    rename_fields: ClassVar[dict[str, str]] = {}

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Rename fields in ``self.fields`` per ``rename_fields`` after the form initializes."""
        super().__init__(*args, **kwargs)
        for key, value in self.rename_fields.items():
            if key != value:
                self.fields[value] = self.fields[key]
                del self.fields[key]


class MatchedObjectGetMixin(_ModelFormHost):
    """
    MatchedObjectGetMixin.

    This class adds methods that
    returns model object or queryset that matches the conditions.
    """

    model: ClassVar[type[Model] | None] = None
    queryset: ClassVar[QuerySet[Any] | None] = None
    raise_exception: ClassVar[bool] = False
    field_lookup: ClassVar[dict[str, str]] = {}

    def get_queryset(self) -> QuerySet[Any]:
        """Return ``queryset``, or fall back to ``model``'s/the form's own default manager."""
        if self.queryset is None:
            if self.model:
                return cast("QuerySet[Any]", self.model._default_manager.all())
            elif hasattr(self, '_meta') and self._meta.model:
                return cast("QuerySet[Any]", self._meta.model._default_manager.all())
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

    def _replace_fields(self, form_data: Mapping[str, Any]) -> dict[str, Any]:
        filter_data = {}
        for k, v in form_data.items():
            filter_data[self.field_lookup.get(k, k)] = v
        return filter_data

    def get_list(self, queryset: QuerySet[Any] | None = None) -> QuerySet[Any]:
        """Return matched object queryset."""
        if queryset is None:
            queryset = self.get_queryset()
        filter_data = self._replace_fields(self.cleaned_data)
        return queryset.filter(**filter_data)

    def get_object(self, queryset: QuerySet[Any] | None = None) -> Any | None:
        """Return matched object."""
        try:
            return self.get_list(queryset).get()
        except (MultipleObjectsReturned, ObjectDoesNotExist) as e:
            if self.raise_exception:
                raise e
            return None


class RelatedModelInlineMixin(_ModelFormHost):
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

    inline_fields: ClassVar[dict[str, Sequence[str]] | None] = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Add form fields for each related model's ``inline_fields`` after the form initializes."""
        super().__init__(*args, **kwargs)
        self._related_field_model: dict[str, type[Model]] = {}
        assert self.inline_fields is not None
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
                    # default=None: a reverse relation may not exist yet.
                    setattr(field_object, 'initial', getattr_chain(
                        self.instance, '%s.%s' % (field, field_name),
                        default=None))
                self.fields['%s_%s' % (field, field_name)] = field_object

    def save(self, commit: bool = True) -> Any:
        """Save the form, then create/update each related model from its ``inline_fields``."""
        object = super().save(commit=False)
        assert self.inline_fields is not None
        inline_fields = self.inline_fields

        def save_inline() -> None:
            for field, related_fields in inline_fields.items():
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
                        assert name is not None
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
                target_field.save()
                setattr(object, rel_pk_field_name, target_field.pk)
                setattr(object, field, target_field)
            object.save()

        if commit:
            save_inline()
            # _save_m2m is BaseModelForm's real internal worker (what Django's
            # own save() calls); django-stubs only declares the public
            # save_m2m, so this needs an ignore rather than the stub's name.
            self._save_m2m()  # type: ignore[attr-defined]
        else:
            # Honor Django's ModelForm.save(commit=False) contract: perform no
            # DB writes now and defer them (plus the base form's own m2m) to
            # save_m2m(). The m2m branch in particular cannot run before the
            # target row exists.
            base_save_m2m = self.save_m2m

            def save_m2m() -> None:
                base_save_m2m()
                save_inline()
            # Same dynamic patch Django's own ModelForm.save(commit=False)
            # does (self.save_m2m = self._save_m2m); django-stubs types
            # save_m2m as a fixed method, so overwriting it needs an ignore.
            self.save_m2m = save_m2m  # type: ignore[method-assign]
        return object

    def _is_many_to_many(self, rel_opts: Any, field_name: str) -> bool:
        for f in rel_opts.many_to_many:
            if f.attname == field_name:
                return True
        return False
