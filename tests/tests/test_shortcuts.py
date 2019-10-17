from django.contrib.auth import get_user_model

from django_boost.shortcuts import (
    get_list_or_default, get_list_or_exception,
    get_object_or_default, get_object_or_exception)
from django_boost.test import TestCase

User = get_user_model()


class TestShortCuts(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.email = 'test@django.boost.com'
        cls.user = User.objects.create(email=cls.email)
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        return super().tearDownClass()

    def test_get_object_or_default(self):
        self.assertEqual(get_object_or_default(
            User, email=self.email, default=1), self.user)
        self.assertEqual(get_object_or_default(
            User, email='no', default=1), 1)

    def test_get_object_or_exception(self):
        class MyException(Exception):
            pass
        with self.assertRaises(MyException):
            get_object_or_exception(User, email='no',
                                    exception=MyException)

    def test_get_list_or_default(self):
        self.assertEqual(
            get_list_or_default(User, email=self.email, default=[]),
            [self.user])

        self.assertEqual(
            get_list_or_default(User, email='no', default=[]),
            [])

    def test_get_list_or_exception(self):
        class MyException(Exception):
            pass
        with self.assertRaises(MyException):
            get_list_or_exception(User, email='no',
                                  exception=MyException)
