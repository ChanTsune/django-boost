from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from .base import ConverterTestCase


class TestConverter(ConverterTestCase):

    def test_path_converters(self):
        case = [('bin', '1010'),
                ('bin', 12),
                ('oct', '7'),
                ('oct', 7),
                ('hex', 'd'),
                ('hex', 12),
                ('bin_str', '1010'),
                ('oct_str', '236'),
                ('hex_str', '234'),
                ('float', 1.1),
                ('float', '1.1'),
                ('float', 1),
                ('float', '1'),
                ]
        for name, value in case:
            with self.subTest(name=name, value=value):
                url = reverse(name, kwargs={name: value})
                response = self.client.get(url)
                self.assertStatusCodeEqual(response, 200)

    def test_float_rejects_trailing_dot(self):
        with self.assertRaises(NoReverseMatch):
            reverse('float', kwargs={'float': '1.'})
