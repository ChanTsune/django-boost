from datetime import datetime, timedelta

from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.timezone import now
from django_boost.views.generic import JsonView, ModelCRUDViews
from django_boost.views.mixins import ReAuthenticationRequiredMixin
from django_boost.views.mixins import RedirectToDetailMixin
from django_boost.views.mixins import LimitedTermMixin
from django_boost.views.mixins import UserAgentMixin
from django_boost.views.mixins import AllowContentTypeMixin
from django_boost.http.response import Http409

from example.models import Customer
from example.forms import CustomerForm


class IndexView(CreateView):
    template_name = "example/index.html"
    extra_context = {"number": -10}
    form_class = CustomerForm
    success_url = reverse_lazy('index')


class CustomerUpdateView(RedirectToDetailMixin, UpdateView):
    template_name = "example/form.html"
    form_class = CustomerForm
    model = Customer
    success_url_name = 'customer_detail'


class CustomerDetailView(DetailView):
    model = Customer
    template_name = "example/detail.html"


class ReloginView(ReAuthenticationRequiredMixin, TemplateView):
    template_name = "example/index.html"
    extra_context = {"number": 1000}
    interval = 30


class StartLimitView(LimitedTermMixin, TemplateView):
    template_name = "example/index.html"

    def get_start_datetime(self):
        return now() + timedelta(hours=1)


class EndLimitView(LimitedTermMixin, TemplateView):
    template_name = "example/index.html"

    def get_end_datetime(self):
        return now() - timedelta(hours=1)


class SELimitView(LimitedTermMixin, TemplateView):
    template_name = "example/index.html"

    def get_start_datetime(self):
        return now() - timedelta(hours=1)

    def get_end_datetime(self):
        return now() + timedelta(hours=1)


class CustomerViews(ModelCRUDViews):
    model = Customer


class JsonSampleView(JsonView):

    def get_context_data(self, **kwargs):
        context = self.json
        return context


class SwichView(UserAgentMixin, TemplateView):
    template_name = "mobile/index.html"
    pc_template_name = "desktop/index.html"
    mobile_template_name = "mobile/index.html"


class Http301View(TemplateView):
    template_name = "example/index.html"

    def get_context_data(self, **kwargs):
        from django_boost.http.response import Http301
        context = super().get_context_data(**kwargs)
        raise Http301('http://google.com')
        return context


class ContentTypeView(AllowContentTypeMixin, TemplateView):
    template_name = "example/index.html"
    allowed_content_types = []
