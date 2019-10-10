import json
import uuid
from json.decoder import JSONDecodeError

from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator, RegexValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


__all__ = ["validate_json", "validate_uuid4", "validate_color_code"]


@deconstructible
class JsonValidator(BaseValidator):

    message = _('Enter valid JSON string.')
    code = 'json value'

    def __init__(self, message=None):
        if message:
            self.message = message

    def __call__(self, value):
        try:
            if isinstance(value, str):
                json.loads(value)
                return
            raise TypeError
        except JSONDecodeError:
            raise ValidationError(self.message, code=self.code)


class ColorCodeValidator(RegexValidator):
    regex = '#[0-9a-fA-F]{6}'
    message = _('Enter 6-digit hexadecimal number including #.')


json_validator = JsonValidator()
color_code_validator = ColorCodeValidator()


def validate_json(value):
    return json_validator(value)


def validate_uuid4(value):
    try:
        uuid_value = uuid.UUID(value)
    except ValueError as e:
        if hasattr(e, 'message'):
            raise ValidationError(e.message)
        else:
            raise ValidationError(str(e))
    if not uuid_value.hex == value.replace("-", ""):
        raise ValidationError("badly formed hexadecimal UUID string")


def validate_color_code(value):
    return color_code_validator(value)
