from django import forms
from .models import Article, Customer


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = '__all__'
