from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

from django_boost.test import TestCase


@override_settings(ROOT_URLCONF='tests.tests.views_mixins.urls')
class UserAgentMixinExtraTests(TestCase):

    def test_user_agent_mixin_requires_extra(self):
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
                self.client.get('/user_agent/')
