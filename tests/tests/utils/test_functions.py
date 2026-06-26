from django_boost.test import TestCase
from django_boost.utils.functions import model_to_json
from tests.models import RelatedItemModel


class ModelToJsonTests(TestCase):

    def test_model_instance_returns_dict(self):
        obj = RelatedItemModel.objects.create(name="x")
        result = model_to_json(obj)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["name"], "x")

    def test_queryset_returns_list_of_dicts(self):
        RelatedItemModel.objects.create(name="a")
        RelatedItemModel.objects.create(name="b")
        queryset = RelatedItemModel.objects.filter(
            name__in=["a", "b"]).order_by("name")
        result = model_to_json(queryset)
        self.assertIsInstance(result, list)
        self.assertEqual([d["name"] for d in result], ["a", "b"])
