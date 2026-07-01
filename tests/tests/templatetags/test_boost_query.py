from django_boost.test import TestCase


class TestBoostQueryTemplateTag(TestCase):

    def setUp(self):
        from tests.models import RelatedItemModel

        items = RelatedItemModel.objects.bulk_create([
            RelatedItemModel(name="bravo"),
            RelatedItemModel(name="alpha"),
            RelatedItemModel(name="charlie"),
        ])
        self.item_ids = [item.pk for item in items]

    def get_queryset(self):
        from tests.models import RelatedItemModel

        return RelatedItemModel.objects.filter(pk__in=self.item_ids)

    def test_filter(self):
        from django_boost.templatetags.boost_query import filter

        queryset = filter(self.get_queryset(), "name=alpha")

        self.assertEqual(list(queryset.values_list("name", flat=True)), ["alpha"])

    def test_exclude(self):
        from django_boost.templatetags.boost_query import exclude

        queryset = exclude(self.get_queryset(), "name=alpha")

        self.assertEqual(
            list(queryset.order_by("name").values_list("name", flat=True)),
            ["bravo", "charlie"],
        )

    def test_filter_value_containing_equals(self):
        from tests.models import RelatedItemModel
        from django_boost.templatetags.boost_query import filter

        item = RelatedItemModel.objects.create(name="a=b=c")
        queryset = RelatedItemModel.objects.filter(pk__in=self.item_ids + [item.pk])

        result = filter(queryset, "name=a=b=c")

        self.assertEqual(list(result.values_list("name", flat=True)), ["a=b=c"])

    def test_exclude_value_containing_equals(self):
        from tests.models import RelatedItemModel
        from django_boost.templatetags.boost_query import exclude

        item = RelatedItemModel.objects.create(name="a=b=c")
        queryset = RelatedItemModel.objects.filter(pk__in=self.item_ids + [item.pk])

        result = exclude(queryset, "name=a=b=c")

        self.assertEqual(
            list(result.order_by("name").values_list("name", flat=True)),
            ["alpha", "bravo", "charlie"],
        )

    def test_order_by(self):
        from django_boost.templatetags.boost_query import order_by

        queryset = order_by(self.get_queryset(), "name")

        self.assertEqual(
            list(queryset.values_list("name", flat=True)),
            ["alpha", "bravo", "charlie"],
        )

    def test_dead_uses_queryset_method_when_available(self):
        from django_boost.templatetags.boost_query import dead

        queryset = QuerySetStub()

        self.assertEqual(dead(queryset), "dead-result")
        self.assertEqual(queryset.calls, ["dead"])

    def test_dead_returns_queryset_without_method(self):
        from django_boost.templatetags.boost_query import dead

        queryset = object()

        self.assertIs(dead(queryset), queryset)

    def test_alive_uses_queryset_method_when_available(self):
        from django_boost.templatetags.boost_query import alive

        queryset = QuerySetStub()

        self.assertEqual(alive(queryset), "alive-result")
        self.assertEqual(queryset.calls, ["alive"])

    def test_alive_returns_queryset_without_method(self):
        from django_boost.templatetags.boost_query import alive

        queryset = object()

        self.assertIs(alive(queryset), queryset)


class QuerySetStub:

    def __init__(self):
        self.calls = []

    def dead(self):
        self.calls.append("dead")
        return "dead-result"

    def alive(self):
        self.calls.append("alive")
        return "alive-result"
