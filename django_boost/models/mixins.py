import uuid

from django.db import models

from django_boost.utils.functions import json_to_model, model_to_json


class JsonMixin:

    def to_json(self, fields=(), exclude=()):
        """Return dict object."""
        return model_to_json(self, fields, exclude)

    @classmethod
    def from_json(cls, dic, fields=(), exclude=()):
        """Generate model instance from dict object."""
        return json_to_model(cls, dic, fields, exclude)


class UUIDModelMixin(models.Model):
    """replace `id` from` AutoField` to `UUIDField`."""

    class Meta:
        abstract = True
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)


class TimeStampModelMixin(models.Model):
    """The fields `posted_at` and `updated_at` are added."""

    class Meta:
        abstract = True
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
