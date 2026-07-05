from __future__ import annotations

import uuid

from django.db import models
from django.db import router
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from django_boost.models.deletion import LogicalDeletionCollector
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

    class Meta:  # noqa: D106
        abstract = True
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True, editable=False)


class TimeStampModelMixin(models.Model):
    """The fields `created_at` and `updated_at` are added."""

    class Meta:  # noqa: D106
        abstract = True
    created_at = models.DateTimeField(verbose_name=_("created date"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("updated date"), auto_now=True)


class LogicalDeletionMixin(models.Model):
    """Provide logical delete."""

    deleted_at = models.DateTimeField(
        verbose_name=_("deleted date"), blank=True, null=True, default=None, editable=False)

    class Meta:  # noqa: D106
        abstract = True

    objects = LogicalDeletionManager()

    @classmethod
    def get_deleted_value(cls):
        return now()

    def delete(self, using=None, keep_parents=False, hard=False, deleted_at=None):
        if hard:
            return super().delete(using=using, keep_parents=keep_parents)
        if self.pk is None:
            raise ValueError(
                "%s object can't be deleted because its %s attribute is set "
                "to None." % (self._meta.object_name, self._meta.pk.attname)
            )
        using = using or router.db_for_write(self.__class__, instance=self)
        collector = LogicalDeletionCollector(using=using, origin=self, deleted_at=deleted_at)
        collector.collect([self], keep_parents=keep_parents)
        return collector.delete()

    def revive(self, force_update=False, using=None):
        """Revive logical deleted item."""
        self.deleted_at = None
        return self.save(force_update=force_update, using=using)

    def is_dead(self):
        """Return True if the item is dead."""
        return self.deleted_at is not None

    def is_alive(self):
        """Return True if record is alive, otherwise False."""
        return self.deleted_at is None
