from django import forms

from django_boost.forms.widgets import Toggleswitch
from django_boost.test.testcase import TestCase


class ToggleswitchTests(TestCase):

    def test_label_for_matches_input_id(self):
        class F(forms.Form):
            t = forms.BooleanField(widget=Toggleswitch, required=False)

        rendered = str(F()['t'])

        self.assertIn('id="id_t"', rendered)
        self.assertIn('for="id_t"', rendered)

    def test_label_for_is_empty_without_an_id(self):
        class F(forms.Form):
            t = forms.BooleanField(widget=Toggleswitch, required=False)

        rendered = str(F(auto_id=False)['t'])

        self.assertNotIn(' id=', rendered)
        self.assertIn('for=""', rendered)
