from django.contrib.admin.sites import site


from django_boost.test.testcase import TestCase

class AdminTest(TestCase):

    def test_register_all(self):
        from django_boost.admin.sites import register_all
        from . import models

        register_all(models)

        self.assertTrue(site.is_registered(models.TestModel))
