from django.db import models

from django_boost.models.mixins import LogicalDeletionMixin


class LogicalDeletionModel(LogicalDeletionMixin):
    name = models.CharField(max_length=8)


class LogicalDeletionParent(LogicalDeletionMixin):
    name = models.CharField(max_length=8)


class LogicalDeletionChild(LogicalDeletionMixin):
    parent = models.ForeignKey(
        LogicalDeletionParent, related_name='children',
        on_delete=models.CASCADE)
    name = models.CharField(max_length=8)


class LogicalDeletionProtectedChild(models.Model):
    parent = models.ForeignKey(
        LogicalDeletionParent, related_name='protected_children',
        on_delete=models.PROTECT)
    name = models.CharField(max_length=8)


class LogicalDeletionNullableChild(LogicalDeletionMixin):
    parent = models.ForeignKey(
        LogicalDeletionParent, related_name='nullable_children',
        null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=8)


def _detach_parent():
    return None


class LogicalDeletionSetChild(LogicalDeletionMixin):
    # on_delete=SET(callable) is non-lazy, so Django evaluates the related
    # queryset during collect() and the FK update is applied to materialized
    # instances (unlike the lazy SET_NULL handler).
    parent = models.ForeignKey(
        LogicalDeletionParent, related_name='set_children',
        null=True, on_delete=models.SET(_detach_parent))
    name = models.CharField(max_length=8)


class PhysicalCascadeChild(models.Model):
    parent = models.ForeignKey(
        LogicalDeletionParent, related_name='physical_children',
        on_delete=models.CASCADE)
    name = models.CharField(max_length=8)


class NonFastPhysicalChild(models.Model):
    # A non-logical child that is NOT fast-deletable: it owns its own cascade
    # grandchild, so Django routes it through Collector.data (not fast_deletes),
    # exercising the physical-delete branch for non-logical models in data.
    parent = models.ForeignKey(
        LogicalDeletionParent, related_name='nonfast_children',
        on_delete=models.CASCADE)
    name = models.CharField(max_length=8)


class NonFastPhysicalGrandChild(models.Model):
    parent = models.ForeignKey(
        NonFastPhysicalChild, related_name='grandchildren',
        on_delete=models.CASCADE)
    name = models.CharField(max_length=8)
