from django_boost.test import TestCase
from django_boost.utils.functions import json_to_model, model_to_json
from tests.models import (ForwardOneToOneModel, RelatedItemModel,
                          ReverseOneToOneModel)


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

    def test_invalid_argument_raises_type_error(self):
        with self.assertRaisesMessage(
            TypeError,
            "model_to_json() argument must be a Model or QuerySet, not str",
        ):
            model_to_json("not-a-model")


class JsonToModelTests(TestCase):

    def test_round_trip_with_relation_field(self):
        r = ReverseOneToOneModel.objects.create(name="r")
        f = ForwardOneToOneModel.objects.create(name="f", forward=r)

        rebuilt = json_to_model(ForwardOneToOneModel, model_to_json(f))

        self.assertEqual(rebuilt.name, "f")
        self.assertEqual(rebuilt.forward_id, r.pk)
