from django_boost.test import TestCase


class TestField(TestCase):
    
    def test_invert_boolean_field(self):
        from django.forms import Form
        from django_boost.forms.fields import InvertBooleanField

        class SampleForm(Form):
            sample = InvertBooleanField(required=False)

        form = SampleForm({'sample': False})
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['sample'])

        form = SampleForm({'sample': True})

        self.assertTrue(form.is_valid())
        self.assertFalse(form.cleaned_data['sample'])
