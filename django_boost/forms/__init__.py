from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

from django_boost.forms.fields import ColorCodeField
from django_boost.forms.mixins import FormUserKwargsMixin
from django_boost.forms.widgets import ColorInput

__all__ = ("ColorCodeField", "ColorInput", "FormUserKwargsMixin",
           "UserCreationForm")

User = get_user_model()


class UserCreationForm(BaseUserCreationForm):

    class Meta:
        model = User
        fields = (User.USERNAME_FIELD,)
