from django.forms.widgets import Input


class ColorInput(Input):
    """HTML <input type='color'>."""

    input_type = 'color'
    template_name = 'django/forms/widgets/input.html'
