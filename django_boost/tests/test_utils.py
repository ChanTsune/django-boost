from django.test import TestCase

from django_boost.utils.functions import loopfirst, loopfirstlast, looplast
# Create your tests here.


class UtilFunctionTest(TestCase):

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
