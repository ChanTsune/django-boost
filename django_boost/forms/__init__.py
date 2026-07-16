"""Extensions for Django's ``django.forms``."""

from __future__ import annotations

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm as BaseAuthenticationForm,
    UserChangeForm as BaseUserChangeForm,
    UserCreationForm as BaseUserCreationForm,
    UsernameField,
)
from django.utils.translation import gettext_lazy as _

from django_boost.forms.fields import ColorCodeField
from django_boost.forms.mixins import FormUserKwargsMixin
from django_boost.forms.widgets import ColorInput

__all__ = (
    "AuthenticationForm",
    "ColorCodeField",
    "ColorInput",
    "FormUserKwargsMixin",
    "UserChangeForm",
    "UserCreationForm",
)


class UserCreationForm(BaseUserCreationForm):
    """A form that creates a user, with no privileges, from the active user model's ``USERNAME_FIELD`` and password."""

    # django-stubs 5.1.3 (CI's Django 4.2 cell) doesn't declare a nested
    # Meta on BaseUserCreationForm (added in a later stubs release);
    # harmless to ignore since the base class is real at runtime in every
    # supported Django version.
    class Meta(BaseUserCreationForm.Meta):  # type: ignore[name-defined]
        """Use the active user model and its ``USERNAME_FIELD`` instead of Django's hardcoded ``username``."""

        model = get_user_model()
        fields = (model.USERNAME_FIELD,)
        field_classes = {
            model.USERNAME_FIELD: UsernameField,
        }


class UserChangeForm(BaseUserChangeForm):
    """A form for changing an existing user, using the active user model's ``USERNAME_FIELD``."""

    # Same cross-stubs-version note as UserCreationForm.Meta above.
    class Meta(BaseUserChangeForm.Meta):  # type: ignore[name-defined]
        """Use the active user model and its ``USERNAME_FIELD`` instead of Django's hardcoded ``username``."""

        model = get_user_model()
        fields = "__all__"
        field_classes = {
            model.USERNAME_FIELD: UsernameField,
        }


class AuthenticationForm(BaseAuthenticationForm):
    """A form for authenticating a user with the active user model's ``USERNAME_FIELD``."""

    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
