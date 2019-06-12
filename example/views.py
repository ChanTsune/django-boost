from datetime import datetime, timedelta

from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy as _
from django_boost.views.generic import JsonView
from django.utils.timezone import now
from django_boost.views.mixins import ReAuthenticationRequiredMixin
from django_boost.views.mixins import RedirectToDetailMixin
from django_boost.views.mixins import LimitedTermMixin
from django_boost.http.response import Http409
from .models import Customer
from .forms import CustomerForm
# Create your views here.


class IndexView(CreateView):
    template_name = "example/index.html"
    extra_context = {"number": -10}
    form_class = CustomerForm
    success_url = _('index')



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
    auth_unnecessary = 30


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

