from django.db import connection
from django.db.models.base import ModelBase
from django_boost.test import TestCase


class TestRelatedModelInlineMixins(TestCase):

    @classmethod
    def setUpClass(cls):
        from tests.models import (
            RelatedItemModel, ForwardOneToOneModel,
            ReverseOneToOneModel,
            ForwardOneToOneHasManyToManyModel,
            ForwardOneToOneHasManyToManyRelatedModel,
            ReverseOneToOneHasManyToManyModel,
            ReverseOneToOneHasManyToManyRelatedModel)
        models = [RelatedItemModel, ForwardOneToOneModel,
                  ReverseOneToOneModel,
                  ForwardOneToOneHasManyToManyModel,
                  ForwardOneToOneHasManyToManyRelatedModel,
                  ReverseOneToOneHasManyToManyModel,
                  ReverseOneToOneHasManyToManyRelatedModel]
        for model in models:
            setattr(cls,model.__name__,model)

    def test_forward_one_to_one(self):
        from .forms import ForwardOneToOneModelForm

    def test_reverse_one_to_one(self):
        from .forms import ReverseOneToOneModelForm

    def test_forward_many_to_many(self):
        from .forms import ForwardOneToOneHasManyToManyModelForm

    def test_reverse_many_to_many(self):
        from .forms import ReverseOneToOneHasManyToManyModelForm

    @classmethod
    def tearDownClass(cls):
        pass

