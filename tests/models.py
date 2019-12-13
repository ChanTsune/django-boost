from django.db import models


class RelatedItemModel(models.Model):
    name = models.CharField(max_length=128)


class ForwardOneToOneModel(models.Model):
    name = models.CharField(max_length=128)
    forward = models.OneToOneField(
        to="ReverseOneToOneModel", related_name='reverse',
        on_delete=models.CASCADE)


class ReverseOneToOneModel(models.Model):
    name = models.CharField(max_length=128)


class ForwardOneToOneHasManyToManyModel(models.Model):
    name = models.CharField(max_length=128)
    forward = models.OneToOneField(
        to='ForwardOneToOneHasManyToManyRelatedModel',
        related_name='reverse', on_delete=models.CASCADE)


class ForwardOneToOneHasManyToManyRelatedModel(models.Model):
    items = models.ManyToManyField(to=RelatedItemModel)


class ReverseOneToOneHasManyToManyModel(models.Model):
    name = models.CharField(max_length=128)


class ReverseOneToOneHasManyToManyRelatedModel(models.Model):
    forward = models.OneToOneField(
        to=ReverseOneToOneHasManyToManyModel,
        related_name='reverse', on_delete=models.CASCADE)
    items = models.ManyToManyField(to=RelatedItemModel)
