from __future__ import annotations

from collections import Counter
from functools import reduce
from operator import attrgetter, or_

from django.core.exceptions import FieldDoesNotExist, ImproperlyConfigured
from django.db import models, transaction
from django.db.models import signals, sql
from django.db.models.deletion import Collector


def get_logical_delete_field(model):
    """Return ``model``'s logical-deletion flag field, or ``None`` if it doesn't use logical deletion."""
    if not hasattr(model, 'get_deleted_value'):
        return None

    get_field_name = getattr(model._default_manager, 'get_deleted_flag_field_name', None)
    if callable(get_field_name):
        field_name = get_field_name()
    else:
        field_name = getattr(model._default_manager, 'delete_flag_field', 'deleted_at')

    try:
        return model._meta.get_field(field_name)
    except FieldDoesNotExist as exc:
        raise ImproperlyConfigured(
            "%s uses logical deletion but its delete flag field '%s' does not "
            "exist." % (model._meta.label, field_name)
        ) from exc


class LogicalDeletionCollector(Collector):

    def __init__(self, using, origin=None, deleted_at=None):
        """Store ``deleted_at`` to use as the logical-deletion timestamp/flag value."""
        super().__init__(using=using, origin=origin)
        self.origin = origin
        self.deleted_at = deleted_at

    def can_fast_delete(self, objs, from_field=None):
        model = getattr(objs, 'model', None)
        if model is None:
            if hasattr(objs, '_meta'):
                model = objs._meta.model
            elif objs:
                model = objs[0].__class__
        if model is not None and get_logical_delete_field(model) is not None:
            return False
        return super().can_fast_delete(objs, from_field=from_field)

    def get_deleted_value(self, model):
        if self.deleted_at is not None:
            return self.deleted_at
        return model.get_deleted_value()

    def delete(self):
        for model, instances in self.data.items():
            self.data[model] = sorted(instances, key=attrgetter('pk'))

        self.sort()
        deleted_counter = Counter()

        with transaction.atomic(using=self.using, savepoint=False):
            for model, obj in self.instances_with_model():
                if not model._meta.auto_created:
                    self._send_delete_signal(signals.pre_delete, model, obj)

            for qs in self.fast_deletes:
                count = qs._raw_delete(using=self.using)
                if count:
                    deleted_counter[qs.model._meta.label] += count

            self._apply_field_updates()

            for instances in self.data.values():
                instances.reverse()

            for model, instances in self.data.items():
                pk_list = [obj.pk for obj in instances]
                if not pk_list:
                    continue

                field = get_logical_delete_field(model)
                if field is None:
                    count = self._delete_batch(model, pk_list)
                else:
                    deleted_value = self.get_deleted_value(model)
                    count = self._logical_delete_batch(model, field, pk_list, deleted_value)
                    for obj in instances:
                        setattr(obj, field.attname, deleted_value)

                if count:
                    deleted_counter[model._meta.label] += count

                if not model._meta.auto_created:
                    for obj in instances:
                        self._send_delete_signal(signals.post_delete, model, obj)

        for model, instances in self.data.items():
            if get_logical_delete_field(model) is not None:
                continue
            for instance in instances:
                setattr(instance, model._meta.pk.attname, None)

        return sum(deleted_counter.values()), dict(deleted_counter)

    def _send_delete_signal(self, signal, model, obj):
        signal.send(sender=model, instance=obj, using=self.using, origin=self.origin)

    def _apply_field_updates(self):
        # Mirror Django's Collector.delete() field-update block: field_updates is
        # {(field, value): [objs, ...]}. The extra in-memory write-back below
        # keeps already-loaded related instances consistent with the DB update.
        for (field, value), instances_list in self.field_updates.items():
            updates = []
            objs = []
            for instances in instances_list:
                if isinstance(instances, models.QuerySet) and instances._result_cache is None:
                    updates.append(instances)
                else:
                    objs.extend(instances)

            if updates:
                combined_updates = reduce(or_, updates)
                combined_updates.update(**{field.name: value})

            if objs:
                model = objs[0].__class__
                pk_list = list({obj.pk for obj in objs})
                query = sql.UpdateQuery(model)
                query.update_batch(pk_list, {field.name: value}, self.using)
                for obj in objs:
                    setattr(obj, field.attname, value)

    def _delete_batch(self, model, pk_list):
        query = sql.DeleteQuery(model)
        return query.delete_batch(pk_list, self.using)

    def _logical_delete_batch(self, model, field, pk_list, deleted_value):
        query = sql.UpdateQuery(model)
        query.update_batch(pk_list, {field.name: deleted_value}, self.using)
        return len(pk_list)
