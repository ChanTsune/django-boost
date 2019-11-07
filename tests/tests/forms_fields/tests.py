from django_boost.test import TestCase


class TestField(TestCase):

    def test_invert_boolean_field(self):
        from django.forms import Form
        from django_boost.forms.fields import InvertBooleanField

        class SampleForm(Form):
            sample = InvertBooleanField(required=False)

        case = [False, True]
        for i in case:
            form = SampleForm({'sample': i})
            self.assertTrue(form.is_valid())
            self.assertEqual(form.cleaned_data['sample'], not i)
