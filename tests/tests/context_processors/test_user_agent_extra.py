from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured
from django.test import RequestFactory

from django_boost.test import TestCase


class UserAgentExtraTests(TestCase):

    def test_user_agent_requires_extra(self):
        from django_boost.context_processors import user_agent

        request = RequestFactory().get('/')
        real_import = __import__

        def import_without_user_agents(name, *args, **kwargs):
            if name == 'user_agents':
                raise ImportError(name)
            return real_import(name, *args, **kwargs)

        with patch('builtins.__import__', import_without_user_agents):
            with self.assertRaisesMessage(
                ImproperlyConfigured,
                "pip install django-boost[useragent]",
            ):
                user_agent(request)
