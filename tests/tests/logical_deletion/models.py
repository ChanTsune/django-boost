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


class PhysicalCascadeChild(models.Model):
    parent = models.ForeignKey(
        LogicalDeletionParent, related_name='physical_children',
        on_delete=models.CASCADE)
    name = models.CharField(max_length=8)
