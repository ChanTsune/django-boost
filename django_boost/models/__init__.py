from django.contrib.auth.models import AbstractUser, UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractEmailUser(AbstractUser):
    """Abstract Email login user model."""

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_(
            'Required. 150 characters or fewer.'
            ' Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email address already exists."),
        },
    )
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta(AbstractUser.Meta):
        abstract = True


class EmailUser(AbstractEmailUser):
    """Email login user model."""

    class Meta(AbstractEmailUser.Meta):
        swappable = 'AUTH_USER_MODEL'
