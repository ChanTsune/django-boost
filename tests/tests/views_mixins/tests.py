import os

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings


ROOT_PATH = os.path.dirname(__file__)


@override_settings(
    ROOT_URLCONF='tests.tests.views_mixins.urls',
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(ROOT_PATH, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django_boost.context_processors.user_agent',
            ],
        },
    }]
)
class TestViewMixins(TestCase):

    @classmethod
    def setUpClass(cls):
        User = get_user_model()
        cls.user = User.objects.create(email="test@test.com", username="test")
        cls.staff_user = User.objects.create(
            email="staff@staff.com", username="staff", is_staff=True)
        cls.super_user = User.objects.create(
            email="super@super.com", username="super", is_superuser=True)
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.staff_user.delete()
        cls.super_user.delete()
        return super().tearDownClass()

    def assertStatusCode(self, response, code):
        self.assertEqual(response.status_code, code)

    def assertStatusCodeIn(self, response, codes):
        self.assertIn(response.status_code, codes)

    def test_allow_content_type(self):
        url = '/content_type_none/'
        response = self.client.get(url)
        self.assertStatusCode(response, 415)

        response = self.client.post(url)
        self.assertStatusCode(response, 415)

        url = '/content_type_allowed/'
        response = self.client.post(url, content_type='text/html')
        self.assertStatusCode(response, 302)

        response = self.client.post(url, content_type='application/xml')
        self.assertStatusCode(response, 415)

    def test_csrf_exempt(self):
        url = '/csrf_exempt/'
        response = self.client.get(url)
        self.assertStatusCode(response, 200)

        response = self.client.post(url)
        self.assertStatusCode(response, 302)

    def test_dynamic_redirect(self):
        url = '/dynamic_redirect/'
        response = self.client.get(url)
        self.assertStatusCode(response, 200)

        response = self.client.post(url)
        self.assertStatusCode(response, 302)
        self.assertEqual(response.url, "/")

        url += "?next=/next/"
        response = self.client.post(url)
        self.assertStatusCode(response, 302)
        self.assertEqual(response.url, "/next/")

    def test_json_request(self):
        url = '/json_request/'
        response = self.client.post(url)
        self.assertStatusCode(response, 302)

        response = self.client.post(url, content_type='application/json')
        self.assertStatusCode(response, 302)

    def test_json_response(self):
        url = '/json_response/'
        response = self.client.get(url)
        self.assertEqual(response.json(), {"json": True})

    def test_limited_term(self):
        url = '/limited_term/'
        response = self.client.get(url)
        self.assertStatusCode(response, 200)

        url = '/limited_term/before/start/'
        response = self.client.get(url)
        self.assertStatusCode(response, 404)

        url = '/limited_term/before/end/'
        response = self.client.get(url)
        self.assertStatusCode(response, 200)

        url = '/limited_term/after/start/'
        response = self.client.get(url)
        self.assertStatusCode(response, 200)

        url = '/limited_term/after/end/'
        response = self.client.get(url)
        self.assertStatusCode(response, 404)

    def test_re_authentication_required(self):
        url = '/re_auth/'
        response = self.client.get(url)
        self.assertStatusCode(response, 302)

        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertStatusCode(response, 200)
        self.client.logout()

    def test_staff_member_required(self):
        url = '/staff_only/'
        response = self.client.get(url)
        self.assertStatusCodeIn(response, [302, 403])

        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertStatusCodeIn(response, [302, 403])
        self.client.logout()

        self.client.force_login(self.staff_user)
        response = self.client.get(url)
        self.assertStatusCode(response, 200)
        self.client.logout()

    def test_superuser_required(self):
        url = '/super_only/'
        response = self.client.get(url)
        self.assertStatusCode(response, 302)

        self.client.force_login(self.super_user)
        response = self.client.get(url)
        self.assertStatusCode(response, 200)
        self.client.logout()

    def test_user_agent(self):
        url = '/user_agent/'
        response = self.client.get(url)
        self.assertStatusCode(response, 200)

    def test_user_kwargs(self):
        url = '/user_kwargs/'
        response = self.client.get(url)
        self.assertStatusCode(response, 200)
