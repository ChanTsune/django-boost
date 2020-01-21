from django_boost.test.testcase import TestCase


class FormTest(TestCase):

    def test_form(self):
        from django_boost.forms import UserCreationForm
        form = UserCreationForm({'email': 'sample@sample.com',
                                 'password1': 'django_boost',
                                 'password2': 'django_boost'
                                 })
        self.assertTrue(form.is_valid())
