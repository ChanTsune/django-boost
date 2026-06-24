from __future__ import annotations

import warnings

from django_boost.contrib.admin_tools.management.commands.adminsitelog import (
    Command,
)

warnings.warn(
    "Running 'adminsitelog' from 'django_boost' is deprecated; add "
    "'django_boost.contrib.admin_tools' to INSTALLED_APPS. The 'django_boost' "
    "command alias will be removed in django-boost 4.0.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ['Command']
