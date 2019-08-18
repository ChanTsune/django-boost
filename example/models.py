from django.db import models

from django_boost.models.mixins import JsonMixin
from django_boost.models.fields import ColorCodeFiled

from django_boost.models.mixins import (UUIDModelMixin, TimeStampModelMixin,
                                        LogicalDeletionMixin)


class Article(UUIDModelMixin, TimeStampModelMixin, LogicalDeletionMixin):
    title = models.CharField(max_length=128)
    text = models.TextField()
    tags = models.ManyToManyField(to="Tag", related_name="articles")


class Tag(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(to="Category", on_delete=models.PROTECT)
    color = ColorCodeFiled(upper=True)


class Category(models.Model):
    name = models.CharField(max_length=64)


class Customer(JsonMixin, models.Model):
    name = models.CharField(max_length=64)
    registered_at = models.DateField(auto_now_add=True)
    color = ColorCodeFiled(upper=True)
