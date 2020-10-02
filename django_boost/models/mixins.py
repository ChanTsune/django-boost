import uuid

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from django_boost.models.manager import LogicalDeletionManager
from django_boost.utils.functions import json_to_model, model_to_json

__all__ = ["JsonMixin", "UUIDModelMixin",
           "TimeStampModelMixin", "LogicalDeletionMixin"]


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
    created_at = models.DateTimeField(verbose_name=_("created date"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("updated date"), auto_now=True)


class LogicalDeletionMixin(models.Model):
    """Provide logical delete."""

    deleted_at = models.DateTimeField(
        verbose_name=_("deleted date"), blank=True, null=True, default=None, editable=False)

    class Meta:
        abstract = True

    objects = LogicalDeletionManager()

    @classmethod
    def get_deleted_value(cls):
        return now()

    def delete(self, using=None, keep_parents=False, hard=False):
        if hard:
            return super().delete(using=using, keep_parents=keep_parents)
        self.deleted_at = self.get_deleted_value()
        return self.save()

    def revive(self, force_update=False, using=None):
        """Revive logical deleted item."""
        self.deleted_at = None
        return self.save()

    def is_dead(self):
        """Return True if the item is dead."""
        return self.deleted_at is not None

    def is_alive(self):
        """Return True if record is alive, otherwise False."""
        return self.deleted_at is None
