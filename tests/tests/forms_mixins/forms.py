from django import forms
from django_boost.forms.mixins import RelatedModelInlineMixin

from tests import models


class ForwardOneToOneModelForm(RelatedModelInlineMixin, forms.ModelForm):
    inline_fields = {'forward': ('name',)}

    class Meta:
        model = models.ForwardOneToOneModel
        fields = ('name',)


class ReverseOneToOneModelForm(RelatedModelInlineMixin, forms.ModelForm):
    inline_fields = {'reverse': ('name',)}

    class Meta:
        model = models.ReverseOneToOneModel
        fields = ('name',)


class ForwardOneToOneHasManyToManyModelForm(RelatedModelInlineMixin, forms.ModelForm):
    inline_fields = {'forward': ('items',)}

    class Meta:
        model = models.ForwardOneToOneHasManyToManyModel
        fields = ('name',)


class ReverseOneToOneHasManyToManyModelForm(RelatedModelInlineMixin, forms.ModelForm):
    inline_fields = {'reverse': ('items',)}

    class Meta:
        model = models.ReverseOneToOneHasManyToManyModel
        fields = ('name',)
