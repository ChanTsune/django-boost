from django.db import models
from django_boost.models.mixins import JsonMixin
from django_boost.models.fields import ColorCodeFiled
# Create your models here.

class Customer(JsonMixin,models.Model):
    name = models.CharField(max_length=64)
    registered_at = models.DateField(auto_now_add=True)
    color = ColorCodeFiled(upper=True)
