"""Custom form widgets for Django's ``django.forms``."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from django.core.files.uploadedfile import UploadedFile
from django.forms.widgets import CheckboxInput, Input, RadioSelect
from django.utils.datastructures import MultiValueDict

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


def boolean_check(v: Any) -> bool:
    return (v is False or v is None or v == '')


class InvertCheckboxInput(CheckboxInput):
    """Returns false if checked, true if not checked."""

    def __init__(
        self,
        attrs: dict[str, Any] | None = None,
        check_test: Callable[[Any], bool] | None = None,
    ) -> None:
        """Fall back to treating ``False``, ``None``, and ``''`` as checked when ``check_test`` is omitted."""
        super().__init__(attrs)
        self.check_test = boolean_check if check_test is None else check_test

    def value_from_datadict(  # noqa: D102
        self,
        data: Mapping[str, Any],
        files: MultiValueDict[str, UploadedFile],
        name: str,
    ) -> bool:
        return not super().value_from_datadict(data, files, name)


class Toggleswitch(CheckboxInput):
    """Toggle switch styled input."""

    template_name = "boost/forms/widgets/toggleswitch.html"
