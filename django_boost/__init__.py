"""Reusable Django extensions: drop-in replacements and add-ons for Django's built-in classes."""

from __future__ import annotations

from django_boost.utils.version import _Version, get_version

VERSION: _Version = (3, 4, 0, 'final', 0)


__version__ = get_version()
