"""This module provides template context functions."""

from __future__ import annotations

from typing import Any

from django.http import HttpRequest

from django_boost.user_agents import parse_user_agent


def user_agent(request: HttpRequest) -> dict[str, Any]:
    """Add parsed user-agent details (browser, device, OS, bot/mobile/tablet flags) to the template context."""
    agent = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse_user_agent(agent)
    context = {'user_agent': agent,
               'browser': user_agent.browser.family,
               'device': user_agent.device.family,
               'is_bot': user_agent.is_bot,
               'is_email_client': user_agent.is_email_client,
               'is_mobile': user_agent.is_mobile,
               'is_pc': user_agent.is_pc,
               'is_tablet': user_agent.is_tablet,
               'is_touch_capable': user_agent.is_touch_capable,
               'os': user_agent.os.family,
               }
    return context
