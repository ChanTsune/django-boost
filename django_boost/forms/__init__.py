from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

from django_boost.forms.fields import ColorCodeField
from django_boost.forms.mixins import FormUserKwargsMixin
from django_boost.forms.widgets import ColorInput

__all__ = ("ColorCodeField", "ColorInput", "FormUserKwargsMixin",
           "UserCreationForm")


class UserCreationForm(BaseUserCreationForm):

    class Meta:
        User = get_user_model()
        model = User
        fields = (User.USERNAME_FIELD,)
