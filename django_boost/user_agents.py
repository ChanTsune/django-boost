"""Lazy access to the optional ``user-agents`` dependency.

``user-agents`` ships only with the ``useragent`` extra, so it is imported
inside the function rather than at module load to keep core installs free of
it.
"""

from __future__ import annotations

from django.core.exceptions import ImproperlyConfigured


def parse_user_agent(agent):
    try:
        from user_agents import parse
    except ImportError as exc:
        raise ImproperlyConfigured(
            "Install user-agent support with "
            "`pip install django-boost[useragent]`."
        ) from exc
    return parse(agent)
