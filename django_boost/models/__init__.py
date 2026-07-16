"""Extensions for Django's ``django.db.models``."""

from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
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

    # django-stubs 5.1.3 (paired with Django 4.2 in CI) doesn't declare a
    # nested Meta on AbstractUser (added in a later stubs release); harmless
    # to ignore since the base class is real at runtime in every version.
    class Meta(AbstractUser.Meta):  # type: ignore[name-defined]  # noqa: D106
        abstract = True


class EmailUser(AbstractEmailUser):
    """Email login user model."""

    class Meta(AbstractEmailUser.Meta):  # noqa: D106
        swappable = 'AUTH_USER_MODEL'
