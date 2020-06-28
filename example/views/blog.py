from django.urls import reverse_lazy

from django_boost.views.generic import (
    ListView, CreateView, DetailView, DeleteView, UpdateView)

from example.models import Article
from example.forms import ArticleForm


class ArticleListView(ListView):
    template_name = "blog/article_list.html"
    model = Article


class ArticleDeletedListView(ListView):
    template_name = "blog/article_list.html"
    queryset = Article.objects.dead()


class ArticleDetail(DetailView):
    template_name = "blog/article_detail.html"
    model = Article


class ArticleCreate(CreateView):
    template_name = "blog/article_create.html"
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy('article_list')


class ArticleUpdate(UpdateView):
    template_name = "blog/article_update.html"
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy('article_list')


class ArticleDelete(DeleteView):
    template_name = "blog/article_delete.html"
    model = Article
    success_url = reverse_lazy('article_list')
