from django.test import TestCase

from django_boost.utils import Loop, isiterable, loop
from django_boost.utils.functions import loopfirst, loopfirstlast, looplast
# Create your tests here.


class TestUtilFunction(TestCase):

    test_list0 = []
    test_list1 = [0]
    test_list2 = [0, 1]
    test_list3 = [0, 1, 2]

    def test_loopfirst(self):
        collect = [True, False, False]
        for is_first, v in loopfirst(self.test_list0):
            self.assertEqual(collect[v], is_first)
        for is_first, v in loopfirst(self.test_list1):
            self.assertEqual(collect[v], is_first)
        for is_first, v in loopfirst(self.test_list2):
            self.assertEqual(collect[v], is_first)
        for is_first, v in loopfirst(self.test_list3):
            self.assertEqual(collect[v], is_first)

    def test_looplast(self):
        for is_last, v in looplast(self.test_list0):
            self.assertEqual([True][v], is_last)
        for is_last, v in looplast(self.test_list1):
            self.assertEqual([True][v], is_last)
        for is_last, v in looplast(self.test_list2):
            self.assertEqual([False, True][v], is_last)
        for is_last, v in looplast(self.test_list3):
            self.assertEqual([False, False, True][v], is_last)

    def test_loopfirstlast(self):
        for is_first_or_last, v in loopfirstlast(self.test_list0):
            self.assertEqual([True][v], is_first_or_last)
        for is_first_or_last, v in loopfirstlast(self.test_list1):
            self.assertEqual([True][v], is_first_or_last)
        for is_first_or_last, v in loopfirstlast(self.test_list2):
            self.assertEqual([True, True][v], is_first_or_last)
        for is_first_or_last, v in loopfirstlast(self.test_list3):
            self.assertEqual([True, False, True][v], is_first_or_last)

    def test_isiterable(self):
        self.assertTrue(isiterable(range(1)))
        self.assertFalse(isiterable(1))


class TestLoop(TestCase):
    items = [0, 1, 2, 3]

    def test_loop_class(self):
        expected_first = [True, False, False, False]
        expected_last = [False, False, False, True]
        expected_counter0 = [0, 1, 2, 3]
        expected_revcounter0 = reversed(expected_counter0)
        for (forloop, _), first, last, counter0, revcounter0 in zip(
            Loop(self.items),
            expected_first,
            expected_last,
            expected_counter0,
                expected_revcounter0):
            self.assertEqual(forloop.first, first)
            self.assertEqual(forloop.last, last)
            self.assertEqual(forloop.counter, counter0 + 1)
            self.assertEqual(forloop.counter0, counter0)
            self.assertEqual(forloop.revcounter, revcounter0 + 1)
            self.assertEqual(forloop.revcounter0, revcounter0)
        for (forloop1, _), (forloop2, _) in zip(
            Loop(self.items),
                loop(self.items)):
            self.assertEqual(forloop1.first, forloop2.first)
            self.assertEqual(forloop1.last, forloop2.last)
            self.assertEqual(forloop1.counter, forloop2.counter)
            self.assertEqual(forloop1.counter0, forloop2.counter0)
            self.assertEqual(forloop1.revcounter, forloop2.revcounter)
            self.assertEqual(forloop1.revcounter0, forloop2.revcounter0)
