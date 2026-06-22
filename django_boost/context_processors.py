"""This module provides template context functions."""

from django_boost.user_agents import parse_user_agent


def user_agent(request):
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
