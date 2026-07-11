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

    def test_reverse_one_to_one_update_without_related_row(self):
        from .forms import ReverseOneToOneModelForm

        # A parent with a pk but no related row yet: the reverse accessor
        # raises RelatedObjectDoesNotExist, which must not break __init__.
        r = self.ReverseOneToOneModel.objects.create(name='orphan')

        form = ReverseOneToOneModelForm(
            {'name': 'sample', 'reverse_name': 'x'}, instance=r)

        self.assertTrue(form.is_valid())
        self.assertIsNone(form.fields['reverse_name'].initial)

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

    def test_reverse_one_to_one_create_commit_false_writes_nothing(self):
        from .forms import ReverseOneToOneModelForm

        Reverse = self.ReverseOneToOneModel
        Forward = self.ForwardOneToOneModel
        form = ReverseOneToOneModelForm(
            {'name': 'sample', 'reverse_name': 'reverse_sample'})
        self.assertTrue(form.is_valid())
        before = Reverse.objects.count()
        forward_before = Forward.objects.count()

        obj = form.save(commit=False)

        self.assertEqual(Reverse.objects.count(), before)
        self.assertEqual(Forward.objects.count(), forward_before)
        self.assertIsNone(obj.pk)

        obj.save()
        form.save_m2m()

        self.assertEqual(Reverse.objects.count(), before + 1)
        self.assertEqual(Forward.objects.count(), forward_before + 1)
        obj.refresh_from_db()
        self.assertEqual(obj.name, 'sample')
        self.assertEqual(obj.reverse.name, 'reverse_sample')

    def test_forward_many_to_many_commit_false_defers_write(self):
        from .forms import ForwardOneToOneHasManyToManyModelForm

        Parent = self.ForwardOneToOneHasManyToManyModel
        Related = self.ForwardOneToOneHasManyToManyRelatedModel
        form = ForwardOneToOneHasManyToManyModelForm(
            {'name': 'sample', 'forward_items': [self.item1.pk]})
        self.assertTrue(form.is_valid())
        parent_before = Parent.objects.count()
        before = Related.objects.count()

        obj = form.save(commit=False)
        self.assertEqual(Parent.objects.count(), parent_before)
        self.assertEqual(Related.objects.count(), before)
        self.assertIsNone(obj.pk)

        form.save_m2m()
        self.assertEqual(Parent.objects.count(), parent_before + 1)
        self.assertEqual(Related.objects.count(), before + 1)
        obj.refresh_from_db()
        self.assertEqual(obj.name, 'sample')
        self.assertEqual(list(obj.forward.items.all()), [self.item1])

    def test_forward_many_to_many_update_commit_false_defers_write(self):
        from .forms import ForwardOneToOneHasManyToManyModelForm

        r = self.ForwardOneToOneHasManyToManyRelatedModel.objects.create()
        r.items.set([self.item1])
        f = self.ForwardOneToOneHasManyToManyModel.objects.create(
            name='-----', forward=r)

        form = ForwardOneToOneHasManyToManyModelForm(
            {'name': 'sample', 'forward_items': [self.item2.pk]},
            instance=f)
        self.assertTrue(form.is_valid())

        obj = form.save(commit=False)
        r.refresh_from_db()
        self.assertEqual(list(r.items.all()), [self.item1])

        form.save_m2m()
        r.refresh_from_db()
        self.assertEqual(list(r.items.all()), [self.item2])
        obj.refresh_from_db()
        self.assertEqual(obj.name, 'sample')

    def test_reverse_many_to_many_commit_false_defers_write(self):
        from .forms import ReverseOneToOneHasManyToManyModelForm

        Parent = self.ReverseOneToOneHasManyToManyModel
        Related = self.ReverseOneToOneHasManyToManyRelatedModel
        form = ReverseOneToOneHasManyToManyModelForm(
            {'name': 'sample', 'reverse_items': [self.item2.pk]})
        self.assertTrue(form.is_valid())
        parent_before = Parent.objects.count()
        before = Related.objects.count()

        obj = form.save(commit=False)
        self.assertEqual(Parent.objects.count(), parent_before)
        self.assertEqual(Related.objects.count(), before)
        self.assertIsNone(obj.pk)

        obj.save()
        self.assertEqual(Related.objects.count(), before)

        form.save_m2m()
        self.assertEqual(Parent.objects.count(), parent_before + 1)
        self.assertEqual(Related.objects.count(), before + 1)
        obj.refresh_from_db()
        self.assertEqual(obj.name, 'sample')
        self.assertEqual(list(obj.reverse.items.all()), [self.item2])

    def test_commit_true_saves_base_forms_own_many_to_many(self):
        from .forms import ReverseOneToOneHasManyToManyRelatedModelForm

        form = ReverseOneToOneHasManyToManyRelatedModelForm(
            {'items': [self.item1.pk], 'forward_name': 'sample'})
        self.assertTrue(form.is_valid())

        obj = form.save()

        obj.refresh_from_db()
        self.assertEqual(list(obj.items.all()), [self.item1])

    @classmethod
    def tearDownClass(cls):
        pass


class TestFieldRenameMixin(TestCase):

    def test_field(self):
        from django import forms
        from django_boost.forms.mixins import FieldRenameMixin

        class MyForm(FieldRenameMixin, forms.Form):
            token_id = forms.CharField()
            rename_fields = {"token_id": "token-id"}

        form = MyForm()

        self.assertIn("token-id", form.fields.keys())
        self.assertNotIn("token_id", form.fields.keys())
