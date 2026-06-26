from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm as BaseUserCreationForm,
    UsernameField,
)

from django_boost.forms.fields import ColorCodeField
from django_boost.forms.mixins import FormUserKwargsMixin
from django_boost.forms.widgets import ColorInput

__all__ = ("ColorCodeField", "ColorInput", "FormUserKwargsMixin",
           "UserCreationForm")


class UserCreationForm(BaseUserCreationForm):
    """
    A form that creates a user, with no privileges, from the active user
    model's ``USERNAME_FIELD`` and password.
    """

    class Meta(BaseUserCreationForm.Meta):
        model = get_user_model()
        fields = (model.USERNAME_FIELD,)
        field_classes = {
            model.USERNAME_FIELD: UsernameField,
        }
