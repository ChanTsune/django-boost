from django.forms.widgets import Input, RadioSelect


class ColorInput(Input):
    """HTML <input type='color'>."""

    input_type = 'color'
    template_name = 'django/forms/widgets/input.html'


class StarRateSelect(RadioSelect):
    """Star styled radio select."""
    template_name = "boost/forms/widgets/star_radio.html"
