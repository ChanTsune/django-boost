from django.forms.widgets import CheckboxInput, Input, RadioSelect

__all__ = ["ColorInput", "InvertCheckboxInput", "PhoneNumberInput"]


class ColorInput(Input):
    """HTML <input type='color'>."""

    input_type = 'color'
    template_name = 'django/forms/widgets/input.html'


class PhoneNumberInput(Input):
    """HTML <input type='tel'>."""

    input_type = 'tel'
    template_name = 'django/forms/widgets/input.html'


class StarRateSelect(RadioSelect):
    """Star styled radio select."""

    template_name = "boost/forms/widgets/star_radio.html"
    option_template_name = "boost/forms/widgets/star_radio_input.html"


def boolean_check(v):
    return (v is False or v is None or v == '')


class InvertCheckboxInput(CheckboxInput):
    """Returns false if checked, true if not checked."""

    def __init__(self, attrs=None, check_test=None):
        super().__init__(attrs)
        self.check_test = boolean_check if check_test is None else check_test

    def value_from_datadict(self, data, files, name):
        return not super().value_from_datadict(data, files, name)


class Toggleswitch(CheckboxInput):
    """toggle switch styled input"""

    template_name = "boost/forms/widgets/toggleswitch.html"
