from django.db import models
from django_boost.models.mixins import LogicalDeletionMixin


class LogicalDeletionModel(LogicalDeletionMixin):
    name = models.CharField(max_length=8)
