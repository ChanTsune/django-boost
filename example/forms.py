from django import forms
from django_boost.forms.fields import StarRateSelect
from .models import Article, Customer


class CustomerForm(forms.ModelForm):
    SELECT = (
        (1,1),
        (2,2),
    )

    radio = forms.ChoiceField(widget=StarRateSelect, choices=SELECT)

    class Meta:
        model = Customer
        fields = '__all__'


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = '__all__'
