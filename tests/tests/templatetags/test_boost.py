from django_boost.test import TestCase


class TestAbs(TestCase):

    def test_returns_absolute_value(self):
        from django_boost.templatetags.boost import _abs

        self.assertEqual(_abs(1), 1)
        self.assertEqual(_abs(-1), 1)
        self.assertEqual(_abs(0), 0)


class TestAll(TestCase):

    def test_returns_true_for_all_truthy_values(self):
        from django_boost.templatetags.boost import _all

        self.assertTrue(_all([True, 1]))
        self.assertTrue(_all([True]))

    def test_returns_false_when_any_value_is_falsey(self):
        from django_boost.templatetags.boost import _all

        self.assertFalse(_all([True, False]))
        self.assertFalse(_all([False, False]))
        self.assertFalse(_all([False]))


class TestAny(TestCase):

    def test_returns_true_when_any_value_is_truthy(self):
        from django_boost.templatetags.boost import _any

        self.assertTrue(_any([False, True]))
        self.assertTrue(_any([True]))
        self.assertTrue(_any([True, False]))

    def test_returns_false_when_all_values_are_falsey(self):
        from django_boost.templatetags.boost import _any

        self.assertFalse(_any([False]))


class TestAscii(TestCase):

    def test_returns_ascii_representation(self):
        from django_boost.templatetags.boost import _ascii

        self.assertEqual(_ascii(1), "1")
        self.assertEqual(_ascii(65), "65")


class TestBin(TestCase):

    def test_returns_binary_string(self):
        from django_boost.templatetags.boost import _bin

        self.assertEqual(_bin(1), "0b1")
        self.assertEqual(_bin(5), "0b101")


class TestBool(TestCase):

    def test_returns_boolean_value(self):
        from django_boost.templatetags.boost import _bool

        self.assertTrue(_bool(1))
        self.assertTrue(_bool([1]))


class TestCallable(TestCase):

    def test_reports_whether_object_is_callable(self):
        from django_boost.templatetags.boost import _callable

        self.assertTrue(_callable(len))


class TestChr(TestCase):

    def test_returns_character_for_codepoint(self):
        from django_boost.templatetags.boost import _chr

        self.assertEqual(_chr(65), "A")


class TestComplex(TestCase):

    def test_returns_complex_number_for_one_argument(self):
        from django_boost.templatetags.boost import _complex

        self.assertEqual(_complex(1), complex(1))

    def test_returns_complex_number_for_two_arguments(self):
        from django_boost.templatetags.boost import _complex

        self.assertEqual(_complex(1, 2), complex(1, 2))


class TestDivmod(TestCase):

    def test_returns_quotient_and_remainder(self):
        from django_boost.templatetags.boost import _divmod

        self.assertEqual(_divmod(7, 3), (2, 1))


class TestFloat(TestCase):

    def test_converts_to_float(self):
        from django_boost.templatetags.boost import _float

        self.assertEqual(_float("3.5"), 3.5)


class TestHex(TestCase):

    def test_returns_hex_string(self):
        from django_boost.templatetags.boost import _hex

        self.assertEqual(_hex(255), "0xff")


class TestId(TestCase):

    def test_returns_object_identity(self):
        from django_boost.templatetags.boost import _id

        value = object()
        self.assertEqual(_id(value), id(value))


class TestInt(TestCase):

    def test_converts_string_to_int(self):
        from django_boost.templatetags.boost import _int

        self.assertEqual(_int("10"), 10)


class TestLen(TestCase):

    def test_returns_length(self):
        from django_boost.templatetags.boost import _len

        self.assertEqual(_len("abc"), 3)


class TestMax(TestCase):

    def test_returns_maximum_value(self):
        from django_boost.templatetags.boost import _max

        self.assertEqual(_max([2, 5, 1]), 5)


class TestMin(TestCase):

    def test_returns_minimum_value(self):
        from django_boost.templatetags.boost import _min

        self.assertEqual(_min([2, 5, 1]), 1)


class TestOct(TestCase):

    def test_returns_octal_string(self):
        from django_boost.templatetags.boost import _oct

        self.assertEqual(_oct(8), "0o10")


class TestOrd(TestCase):

    def test_returns_codepoint_value(self):
        from django_boost.templatetags.boost import _ord

        self.assertEqual(_ord("A"), 65)


class TestPow(TestCase):

    def test_returns_power_value(self):
        from django_boost.templatetags.boost import _pow

        self.assertEqual(_pow(2, 3), 8)


class TestRound(TestCase):

    def test_rounds_without_ndigits(self):
        from django_boost.templatetags.boost import _round

        self.assertEqual(_round(1.234), 1)

    def test_rounds_with_ndigits(self):
        from django_boost.templatetags.boost import _round

        self.assertEqual(_round(1.234, 2), 1.23)


class TestSum(TestCase):

    def test_returns_total(self):
        from django_boost.templatetags.boost import _sum

        self.assertEqual(_sum([1, 2, 3]), 6)


class TestType(TestCase):

    def test_returns_type_object(self):
        from django_boost.templatetags.boost import _type

        self.assertIs(_type(1), int)


class TestEnumerate(TestCase):

    def test_starts_at_zero_by_default(self):
        from django_boost.templatetags.boost import _enumerate

        self.assertEqual(list(_enumerate(["a", "b"])), [(0, "a"), (1, "b")])

    def test_accepts_custom_start_value(self):
        from django_boost.templatetags.boost import _enumerate

        self.assertEqual(list(_enumerate(["a", "b"], 1)), [(1, "a"), (2, "b")])


class TestDir(TestCase):

    def test_lists_attributes(self):
        from django_boost.templatetags.boost import _dir

        self.assertIn("__class__", _dir(object()))


class TestFormat(TestCase):

    def test_formats_without_format_spec(self):
        from django_boost.templatetags.boost import _format

        self.assertEqual(_format(3), "3")

    def test_formats_with_format_spec(self):
        from django_boost.templatetags.boost import _format

        self.assertEqual(_format(3, "04d"), "0003")


class TestGetattr(TestCase):

    def test_returns_attribute_value(self):
        from django_boost.templatetags.boost import _getattr

        class Example:
            value = 3

        self.assertEqual(_getattr(Example(), "value"), 3)


class TestHasattr(TestCase):

    def test_reports_attribute_presence(self):
        from django_boost.templatetags.boost import _hasattr

        class Example:
            value = 3

        self.assertTrue(_hasattr(Example(), "value"))


class TestHash(TestCase):

    def test_returns_hash_value(self):
        from django_boost.templatetags.boost import _hash

        self.assertEqual(_hash("x"), hash("x"))


class TestRange(TestCase):

    def test_returns_range_for_one_argument(self):
        from django_boost.templatetags.boost import _range

        self.assertEqual(list(_range(3)), [0, 1, 2])

    def test_returns_range_for_two_arguments(self):
        from django_boost.templatetags.boost import _range

        self.assertEqual(list(_range(1, 4)), [1, 2, 3])


class TestRepr(TestCase):

    def test_returns_repr_string(self):
        from django_boost.templatetags.boost import _repr

        class Example:
            value = 3

        example = Example()
        self.assertEqual(_repr(example), repr(example))


class TestReversed(TestCase):

    def test_reverses_sequence(self):
        from django_boost.templatetags.boost import _reversed

        self.assertEqual(list(_reversed([1, 2, 3])), [3, 2, 1])


class TestSorted(TestCase):

    def test_sorts_iterable(self):
        from django_boost.templatetags.boost import _sorted

        self.assertEqual(_sorted([3, 1, 2]), [1, 2, 3])


class TestStr(TestCase):

    def test_converts_to_string(self):
        from django_boost.templatetags.boost import _str

        self.assertEqual(_str(5), "5")


class TestVars(TestCase):

    def test_returns_instance_variables(self):
        from django_boost.templatetags.boost import _vars

        class Example:
            value = 3

        example = Example()
        example.value = 3
        self.assertIn("value", _vars(example))


class TestIter(TestCase):

    def test_returns_iterator(self):
        from django_boost.templatetags.boost import _iter

        iterator = _iter([1, 2, 3])
        self.assertEqual(next(iterator), 1)
        self.assertEqual(next(iterator), 2)


class TestNext(TestCase):

    def test_returns_next_item_without_default(self):
        from django_boost.templatetags.boost import _next

        iterator = iter([10, 20, 30])
        self.assertEqual(_next(iterator), 10)

    def test_returns_default_when_provided(self):
        from django_boost.templatetags.boost import _next

        iterator = iter([10, 20, 30])
        self.assertEqual(_next(iterator), 10)
        self.assertEqual(_next(iterator, "fallback"), 20)


class TestZip(TestCase):

    def test_returns_pairs(self):
        import warnings

        from django_boost.templatetags.boost import _zip

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = _zip([1, 2], [3, 4])

        self.assertEqual(caught, [])
        self.assertEqual(list(result), [(1, 3), (2, 4)])


class TestDelattr(TestCase):

    def test_removes_attribute(self):
        from django_boost.templatetags.boost import _delattr

        class Example:
            pass

        example = Example()
        example.value = 3

        self.assertEqual(_delattr(example, "value"), example)
        self.assertFalse(hasattr(example, "value"))


class TestSetattr(TestCase):

    def test_sets_attribute(self):
        from django_boost.templatetags.boost import _setattr

        class Example:
            pass

        example = Example()

        self.assertEqual(_setattr(example, "value", 4), example)
        self.assertEqual(example.value, 4)


class TestZipTag(TestCase):

    def test_returns_zipped_pairs(self):
        from django_boost.templatetags.boost import _zip_tag

        self.assertEqual(list(_zip_tag([1, 2], [3, 4])), [(1, 3), (2, 4)])


class TestZipLongest(TestCase):

    def test_returns_longest_zipped_rows(self):
        from django_boost.templatetags.boost import _zip_longest

        self.assertEqual(list(_zip_longest([1, 2], [3, 4], [5])), [(1, 3, 5), (2, 4, None)])


class TestChain(TestCase):

    def test_returns_chained_values(self):
        from django_boost.templatetags.boost import _chain

        self.assertEqual(list(_chain([1, 2], [3, 4])), [1, 2, 3, 4])


class TestVar(TestCase):

    def test_returns_input_value(self):
        from django_boost.templatetags.boost import var

        value = object()
        self.assertIs(var(value), value)


class TestList(TestCase):

    def test_materializes_iterator(self):
        from django_boost.templatetags.boost import _list

        self.assertEqual(_list(iter([1, 2, 3])), [1, 2, 3])


class TestTuple(TestCase):

    def test_materializes_iterator(self):
        from django_boost.templatetags.boost import _tuple

        self.assertEqual(_tuple(iter([1, 2, 3])), (1, 2, 3))


class TestSet(TestCase):

    def test_deduplicates_iterable(self):
        from django_boost.templatetags.boost import _set

        self.assertEqual(_set([1, 2, 2, 3]), {1, 2, 3})


class TestFrozenset(TestCase):

    def test_deduplicates_iterable(self):
        from django_boost.templatetags.boost import _frozenset

        self.assertEqual(_frozenset([1, 2, 2, 3]), frozenset({1, 2, 3}))


class TestDict(TestCase):

    def test_builds_from_pairs(self):
        from django_boost.templatetags.boost import _dict

        self.assertEqual(_dict([("a", 1), ("b", 2)]), {"a": 1, "b": 2})
