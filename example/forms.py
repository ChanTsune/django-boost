from __future__ import annotations

from typing import Any

from django import forms

from django_boost.forms.widgets import StarRateSelect

from .models import Article, Customer


class CustomerForm(forms.ModelForm):
    SELECT = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    radio = forms.ChoiceField(
        label="Rating",
        widget=StarRateSelect,
        choices=SELECT,
        initial=4,
    )

    class Meta:
        model = Customer
        fields = '__all__'
        labels = {
            'name': 'Customer name',
            'color': 'Favorite color',
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if not self.is_bound and not self.instance.pk:
            self.fields['color'].initial = '#0F9F7D'


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = '__all__'
