from django import forms
from django.test import RequestFactory
from django.views.generic import CreateView, UpdateView

from django_boost.test import TestCase
from django_boost.views.generic import ModelCRUDViews
from tests.models import RelatedItemModel


class ItemForm(forms.ModelForm):
    class Meta:
        model = RelatedItemModel
        fields = ["name"]


class ItemCreateView(CreateView):
    form_class = ItemForm


class ItemUpdateView(UpdateView):
    form_class = ItemForm


class ItemCRUD(ModelCRUDViews):
    model = RelatedItemModel
    success_url = "/done/"
    create_view = ItemCreateView
    update_view = ItemUpdateView


class ModelCRUDViewsFormClassTests(TestCase):
    """ModelCRUDViews must respect a view's own form_class / fields instead of
    forcing fields='__all__' (an ImproperlyConfigured alongside form_class)."""

    def setUp(self):
        self.factory = RequestFactory()

    def test_create_with_form_class(self):
        response = ItemCRUD().create(self.factory.post("/", data={"name": "x"}))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/done/")
        self.assertTrue(RelatedItemModel.objects.filter(name="x").exists())

    def test_update_with_form_class(self):
        item = RelatedItemModel.objects.create(name="old")

        response = ItemCRUD().update(
            self.factory.post("/", data={"name": "new"}), pk=item.pk)

        self.assertEqual(response.status_code, 302)
        item.refresh_from_db()
        self.assertEqual(item.name, "new")

    def test_fields_default_only_without_view_form_config(self):
        crud = ItemCRUD()

        class PlainView(CreateView):
            pass

        class FieldsView(CreateView):
            fields = ["name"]

        self.assertNotIn("fields", crud._form_view_kwargs(ItemCreateView))
        self.assertNotIn("fields", crud._form_view_kwargs(FieldsView))
        self.assertEqual(crud._form_view_kwargs(PlainView)["fields"], "__all__")
