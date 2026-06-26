from django_boost.test.testcase import TestCase


class FormTest(TestCase):

    def test_form(self):
        from django_boost.forms import UserCreationForm
        form = UserCreationForm({'email': 'sample@sample.com',
                                 'password1': 'django_boost',
                                 'password2': 'django_boost'
                                 })
        self.assertTrue(form.is_valid())

    def test_user_creation_form_applies_usernamefield_to_identifier(self):
        from django.contrib.auth import get_user_model
        from django.contrib.auth.forms import UsernameField
        from django_boost.forms import UserCreationForm

        form = UserCreationForm()
        identifier_field = get_user_model().USERNAME_FIELD

        self.assertIsInstance(form.fields[identifier_field], UsernameField)

    def test_user_creation_form_saves_user(self):
        from django.contrib.auth import get_user_model
        from django_boost.forms import UserCreationForm

        form = UserCreationForm({'email': 'created@sample.com',
                                 'password1': 'django_boost',
                                 'password2': 'django_boost'
                                 })
        self.assertTrue(form.is_valid())
        user = form.save()

        self.assertEqual(user.email, 'created@sample.com')
        self.assertTrue(
            get_user_model().objects.filter(email='created@sample.com').exists())
