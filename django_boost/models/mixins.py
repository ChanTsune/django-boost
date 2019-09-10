import uuid

from django.db import models
from django.utils.timezone import now

from django_boost.models.manager import LogicalDeletionManager
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
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True, editable=False)


class TimeStampModelMixin(models.Model):
    """The fields `posted_at` and `updated_at` are added."""

    class Meta:
        abstract = True
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LogicalDeletionMixin(models.Model):
    """Provide logical delete."""

    deleted_at = models.DateTimeField(
        verbose_name="deleted_at", blank=True, null=True, default=None)

    class Meta:
        abstract = True

    objects = LogicalDeletionManager()

    def get_deleted_value(self):
        return now()

    def delete(self, using=None, keep_parents=False, hard=False):
        if hard:
            return super().delete(using=using, keep_parents=keep_parents)
        self.deleted_at = self.get_deleted_value()
        return self.save()
