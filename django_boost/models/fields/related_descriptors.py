from django.db.models.fields.related_descriptors import (
    ReverseOneToOneDescriptor)
from django.db.transaction import atomic


class AutoReverseOneToOneDescriptor(ReverseOneToOneDescriptor):
    """
    ReverseOneToOneDescriptor for AutoOneToOneField.

    The descriptor that handles the object creation for an AutoOneToOneField.
    """

    @atomic
    def __get__(self, instance, cls=None):
        model = getattr(self.related, 'related_model', self.related.model)
        try:
            return super().__get__(instance, cls)
        except model.DoesNotExist:
            obj, _ = model.objects.get_or_create(
                **{self.related.field.name: instance})

            self.related.set_cached_value(instance, obj)
            self.related.field.set_cached_value(obj, instance)
            return obj
