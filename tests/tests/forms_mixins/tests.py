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
            setattr(cls, model.__name__, model)
        cls.item1 = RelatedItemModel.objects.create(name='item1')
        cls.item2 = RelatedItemModel.objects.create(name='item2')

    def test_forward_one_to_one_create(self):
        from .forms import ForwardOneToOneModelForm

        form = ForwardOneToOneModelForm(
            {'name': 'sample', 'forward_name': 'forward_sample'})
        self.assertTrue(form.is_valid())
        form.save()

    def test_forward_one_to_one_update(self):
        from .forms import ForwardOneToOneModelForm
        r = self.ReverseOneToOneModel.objects.create(name='+++++')
        f = self.ForwardOneToOneModel.objects.create(name='-----', forward=r)

        form = ForwardOneToOneModelForm(
            {'name': 'sample', 'forward_name': 'forward_sample'}, instance=f)
        self.assertTrue(form.is_valid())
        form.save()

    def test_reverse_one_to_one_create(self):
        from .forms import ReverseOneToOneModelForm

        form = ReverseOneToOneModelForm(
            {'name': 'sample', 'reverse_name': 'reverse_sample'})
        self.assertTrue(form.is_valid())
        form.save()

    def test_reverse_one_to_one_update(self):
        from .forms import ReverseOneToOneModelForm
        r = self.ReverseOneToOneModel.objects.create(name='+++++')
        _ = self.ForwardOneToOneModel.objects.create(name='-----', forward=r)

        form = ReverseOneToOneModelForm(
            {'name': 'sample', 'reverse_name': 'reverse_sample'}, instance=r)
        self.assertTrue(form.is_valid())
        form.save()

    def test_forward_many_to_many_create(self):
        from .forms import ForwardOneToOneHasManyToManyModelForm

        form = ForwardOneToOneHasManyToManyModelForm(
            {'name': 'sample', 'forward_items': [self.item1.pk]})
        self.assertTrue(form.is_valid())
        form.save()

    def test_forward_many_to_many_update(self):
        from .forms import ForwardOneToOneHasManyToManyModelForm

        i = self.RelatedItemModel.objects.create(name='sample_item')
        r = self.ForwardOneToOneHasManyToManyRelatedModel.objects.create()
        r.items.set([i])
        r.save()
        f = self.ForwardOneToOneHasManyToManyModel.objects.create(
            name='-----', forward=r)
        form = ForwardOneToOneHasManyToManyModelForm(
            {'name': 'sample', 'forward_items': [self.item1.pk]}, instance=f)
        self.assertTrue(form.is_valid())
        form.save()

    def test_reverse_many_to_many_create(self):
        from .forms import ReverseOneToOneHasManyToManyModelForm

        form = ReverseOneToOneHasManyToManyModelForm(
            {'name': 'sample', 'reverse_items': [self.item2.pk]})
        self.assertTrue(form.is_valid())
        form.save()

    def test_reverse_many_to_many_update(self):
        from .forms import ReverseOneToOneHasManyToManyModelForm

        i = self.RelatedItemModel.objects.create(name='sample_item')
        r = self.ReverseOneToOneHasManyToManyModel.objects.create(name='=====')
        f = self.ReverseOneToOneHasManyToManyRelatedModel.objects.create(
            forward=r)
        f.items.set([i])
        f.save()

        form = ReverseOneToOneHasManyToManyModelForm(
            {'name': 'sample', 'reverse_items': [self.item2.pk]}, instance=r)
        self.assertTrue(form.is_valid())
        form.save()

    @classmethod
    def tearDownClass(cls):
        pass
