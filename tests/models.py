from django.db import models
from django_boost.models.fields import AutoOneToOneField


class RelatedItemModel(models.Model):
    name = models.CharField(max_length=128)


class ForwardOneToOneModel(models.Model):
    name = models.CharField(max_length=128)
    forward = models.OneToOneField(
        to="ReverseOneToOneModel", related_name='reverse', on_delete=models.CASCADE)


class ReverseOneToOneModel(models.Model):
    name = models.CharField(max_length=128)


class ForwardOneToOneHasManyToManyModel(models.Model):
    forward = models.OneToOneField(
        to='ForwardOneToOneHasManyToManyRelatedModel', related_name='reverse', on_delete=models.CASCADE)


class ForwardOneToOneHasManyToManyRelatedModel(models.Model):
    items = models.ManyToManyField(to=RelatedItemModel)


class ReverseOneToOneHasManyToManyModel(models.Model):
    pass

class ReverseOneToOneHasManyToManyRelatedModel(models.Model):
    forward = models.OneToOneField(
        to=ReverseOneToOneHasManyToManyModel, related_name='reverse', on_delete=models.CASCADE)
    items = models.ManyToManyField(to=RelatedItemModel)


## テストケース
# 自身が持つOneToOne先に外部キーがある場合
# 自身が持つOneToOne先にManyToManyがある場合
# 自身に対してOneToOneに対して自身が外部キーを持つ場合
# 自身に対してOneToOneに対して自身がManyToManyを持つ場合
