import os

from django.test import TestCase, override_settings


ROOT_PATH = os.path.dirname(__file__)


USER_AGENT_PC = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) '
'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
USER_AGENT_MOBILE = 'Mozilla/5.0 (Mobile; Windows Phone 8.1; '
'Android 4.0; ARM; Trident/7.0; Touch; rv:11.0; IEMobile/11.0; '
'HTC; Windows Phone 8X by HTC) like iPhone OS 7_0_3 Mac OS X '
'AppleWebKit/537 (KHTML, like Gecko) Mobile Safari/537'
USER_AGENT_TABLET = 'Mozilla/5.0 (iPad; CPU OS 10_0 like Mac OS X) '
'AppleWebKit/602.1.32 (KHTML, like Gecko) Version/10.0 Mobile/14A5261v '
'Safari/602.1'
USER_AGENT_UNKNOWN = ''
TEST_DATA = [
    (USER_AGENT_PC, 'PC', True),
    (USER_AGENT_PC, 'MOBILE', False),
    (USER_AGENT_PC, 'TABLET', False),
    (USER_AGENT_PC, 'UNKNOWN', False),

    (USER_AGENT_MOBILE, 'PC', False),
    (USER_AGENT_MOBILE, 'MOBILE', True),
    (USER_AGENT_MOBILE, 'TABLET', False),
    (USER_AGENT_MOBILE, 'UNKNOWN', False),

    (USER_AGENT_TABLET, 'PC', False),
    (USER_AGENT_TABLET, 'MOBILE', False),
    (USER_AGENT_TABLET, 'TABLET', True),
    (USER_AGENT_TABLET, 'UNKNOWN', False),

    (USER_AGENT_UNKNOWN, 'PC', False),
    (USER_AGENT_UNKNOWN, 'MOBILE', False),
    (USER_AGENT_UNKNOWN, 'TABLET', False),
    (USER_AGENT_UNKNOWN, 'UNKNOWN', True),

]


@override_settings(
    ROOT_URLCONF='django_boost.tests.context_processors.urls',
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(ROOT_PATH, 'context_processors', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django_boost.context_processors.user_agent',
            ],
        },
    }]
)
class TestConTextProcessors(TestCase):

    url = ''

    def test_user_agent(self):
        for user_agent, value, exc in TEST_DATA:
            with self.subTest("{}_{}_{}".format(user_agent,
                                                value, exc), value=value):
                self.client = self.client_class(HTTP_USER_AGENT=user_agent)
                response = self.client.get(self.url)
                if exc:
                    self.assertContains(response, value)
                else:
                    self.assertNotContains(response, value)
