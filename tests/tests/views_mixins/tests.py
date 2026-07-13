import os

from django.contrib.auth import get_user_model
from django.test import override_settings

from django_boost.test import TestCase

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

    def test_allow_content_type(self):
        url = '/content_type_none/'
        response = self.client.get(url)
        self.assertStatusCodeEqual(response, 415)

        response = self.client.post(url)
        self.assertStatusCodeEqual(response, 415)

        url = '/content_type_allowed/'
        response = self.client.post(url, content_type='text/html')
        self.assertStatusCodeEqual(response, 302)

        response = self.client.post(url, content_type='application/xml')
        self.assertStatusCodeEqual(response, 415)

    def test_csrf_exempt(self):
        url = '/csrf_exempt/'
        response = self.client.get(url)
        self.assertStatusCodeEqual(response, 200)

        response = self.client.post(url)
        self.assertStatusCodeEqual(response, 302)

    def test_dynamic_redirect(self):
        url = '/dynamic_redirect/'
        response = self.client.get(url)
        self.assertStatusCodeEqual(response, 200)

        response = self.client.post(url)
        self.assertStatusCodeEqual(response, 302)
        self.assertEqual(response.url, "/")

        url += "?next=/next/"
        response = self.client.post(url)
        self.assertStatusCodeEqual(response, 302)
        self.assertEqual(response.url, "/next/")

    def test_json_request(self):
        url = '/json_request/'
        response = self.client.post(url)
        self.assertStatusCodeEqual(response, 302)

        response = self.client.post(url, content_type='application/json')
        self.assertStatusCodeEqual(response, 302)

    def test_json_response(self):
        url = '/json_response/'
        response = self.client.get(url)
        self.assertEqual(response.json(), {"json": True})

    def test_limited_term(self):
        url = '/limited_term/'
        response = self.client.get(url)
        self.assertStatusCodeEqual(response, 200)

        url = '/limited_term/before/start/'
        response = self.client.get(url)
        self.assertStatusCodeEqual(response, 404)

        url = '/limited_term/before/end/'
        response = self.client.get(url)
        self.assertStatusCodeEqual(response, 200)

        url = '/limited_term/after/start/'
        response = self.client.get(url)
        self.assertStatusCodeEqual(response, 200)

        url = '/limited_term/after/end/'
        response = self.client.get(url)
        self.assertStatusCodeEqual(response, 404)

    def test_re_authentication_required(self):
        url = '/re_auth/'
        response = self.client.get(url)
        self.assertStatusCodeEqual(response, 302)

        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertStatusCodeEqual(response, 200)
        self.client.logout()

    def test_re_authentication_required_logout(self):
        from django.contrib.auth import get_user

        self.client.force_login(self.user)
        response = self.client.get('/re_auth/logout/')
        self.assertStatusCodeEqual(response, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/re_auth/logout/')
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_anonymous_required(self):
        url = '/anonymous_only/'
        response = self.client.get(url)
        self.assertStatusCodeEqual(response, 200)

        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertStatusCodeEqual(response, 302)
        self.client.logout()

    @override_settings(LOGIN_REDIRECT_URL='/accounts/profile/')
    def test_anonymous_required_redirects_to_login_redirect_url(self):
        self.client.force_login(self.user)
        response = self.client.get('/anonymous_only/')
        self.assertEqual(response.url, '/accounts/profile/')
        self.client.logout()

    def test_anonymous_required_honors_redirect_authenticated_url(self):
        self.client.force_login(self.user)
        response = self.client.get('/anonymous_only/custom/')
        self.assertStatusCodeEqual(response, 302)
        self.assertEqual(response.url, '/custom/')
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
        self.assertStatusCodeEqual(response, 200)
        self.client.logout()

    def test_superuser_required(self):
        url = '/super_only/'
        response = self.client.get(url)
        self.assertStatusCodeEqual(response, 302)

        self.client.force_login(self.super_user)
        response = self.client.get(url)
        self.assertStatusCodeEqual(response, 200)
        self.client.logout()

    def test_user_agent(self):
        url = '/user_agent/'
        response = self.client.get(url)
        self.assertStatusCodeEqual(response, 200)

    def test_user_kwargs(self):
        url = '/user_kwargs/'
        response = self.client.get(url)
        self.assertStatusCodeEqual(response, 200)


class JsonRequestMixinBodyTests(TestCase):
    """JsonRequestMixin.json honors a declared charset and falls back to {}
    for an unreadable body, the same as for malformed JSON."""

    def _json_for(self, body, content_type="application/json"):
        from django.test import RequestFactory

        from tests.tests.views_mixins.views import JsonRequestView

        view = JsonRequestView()
        view.request = RequestFactory().generic("POST", "/", data=body,
                                                content_type=content_type)
        return view.json

    def test_respects_declared_charset(self):
        body = '{"k": "あ"}'.encode("shift_jis")
        self.assertEqual(
            self._json_for(body, "application/json; charset=shift_jis"),
            {"k": "あ"})

    def test_non_utf8_body_falls_back_to_empty_dict(self):
        self.assertEqual(self._json_for(b"\xff\xfe"), {})

    def test_malformed_json_falls_back_to_empty_dict(self):
        self.assertEqual(self._json_for(b"{"), {})

    def test_valid_utf8_json_is_parsed(self):
        self.assertEqual(self._json_for(b'{"a": 1}'), {"a": 1})


class ReAuthenticationRequiredMixinTests(TestCase):
    """need_reauthentication must handle an authenticated user whose
    last_login is None (never logged in / no update_last_login)."""

    class _User:
        def __init__(self, last_login):
            self.last_login = last_login

    def setUp(self):
        from django_boost.views.mixins import ReAuthenticationRequiredMixin
        self.mixin = ReAuthenticationRequiredMixin()

    def test_requires_reauth_when_last_login_is_none(self):
        from datetime import timedelta
        self.assertTrue(
            self.mixin.need_reauthentication(self._User(None), timedelta(hours=1)))

    def test_no_reauth_when_recently_logged_in(self):
        from datetime import timedelta
        from django.utils.timezone import now
        self.assertFalse(
            self.mixin.need_reauthentication(self._User(now()), timedelta(hours=1)))

    def test_requires_reauth_when_login_is_stale(self):
        from datetime import timedelta
        from django.utils.timezone import now
        self.assertTrue(self.mixin.need_reauthentication(
            self._User(now() - timedelta(hours=2)), timedelta(hours=1)))


class JsonResponseMixinContextTests(TestCase):
    """get_context_data must not mutate or alias the class-level extra_context,
    otherwise request-specific kwargs leak into later requests."""

    def _view_class(self):
        from django_boost.views.mixins import JsonResponseMixin

        class V(JsonResponseMixin):
            extra_context = {'site': 'x'}
        return V

    def test_does_not_mutate_class_extra_context(self):
        V = self._view_class()
        V().get_context_data(pk=1)
        self.assertEqual(V.extra_context, {'site': 'x'})

    def test_does_not_leak_kwargs_across_instances(self):
        V = self._view_class()
        V().get_context_data(pk=1)
        self.assertEqual(V().get_context_data(), {'site': 'x'})

    def test_returns_a_fresh_dict_not_the_class_attribute(self):
        V = self._view_class()
        context = V().get_context_data(pk=1)
        self.assertEqual(context, {'site': 'x', 'pk': 1})
        self.assertIsNot(context, V.extra_context)


class JsonResponseMixinResponseClassTests(TestCase):
    """JsonResponseMixin.get must build the response with the configured
    response_class, not a hardcoded JsonResponse."""

    def test_get_uses_configured_response_class(self):
        from django.http import JsonResponse
        from django.test import RequestFactory

        from django_boost.views.mixins import JsonResponseMixin

        class MyJsonResponse(JsonResponse):
            pass

        class V(JsonResponseMixin):
            response_class = MyJsonResponse

        response = V().get(RequestFactory().get("/"))
        self.assertIsInstance(response, MyJsonResponse)


class DynamicRedirectMixinModelFormTests(TestCase):
    """DynamicRedirectMixin must not bypass ModelFormMixin.get_success_url()'s
    success_url interpolation or its get_absolute_url() fallback."""

    def test_interpolates_success_url_placeholder(self):
        from django.test import RequestFactory
        from django.views.generic import CreateView

        from django_boost.views.mixins import DynamicRedirectMixin
        from tests.models import RelatedItemModel

        class V(DynamicRedirectMixin, CreateView):
            model = RelatedItemModel
            fields = ['name']
            success_url = '/items/{id}/'

        view = V()
        view.request = RequestFactory().post('/')
        view.object = RelatedItemModel.objects.create(name='x')

        self.assertEqual(view.get_success_url(), '/items/%d/' % view.object.pk)

    def test_falls_back_to_get_absolute_url_when_success_url_unset(self):
        from django.test import RequestFactory
        from django.views.generic import CreateView

        from django_boost.views.mixins import DynamicRedirectMixin
        from tests.models import RelatedItemModel

        class V(DynamicRedirectMixin, CreateView):
            model = RelatedItemModel
            fields = ['name']

        view = V()
        view.request = RequestFactory().post('/')
        view.object = RelatedItemModel.objects.create(name='y')

        self.assertEqual(view.get_success_url(), view.object.get_absolute_url())
