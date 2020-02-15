from datetime import timedelta

from django.forms import Form
from django.utils.timezone import now
from django.views.generic import FormView, TemplateView, View

from django_boost.forms.mixins import FormUserKwargsMixin
from django_boost.views.generic import TemplateView as BoostTemplateView
from django_boost.views.mixins import (AllowContentTypeMixin, CSRFExemptMixin,
                                       DynamicRedirectMixin, JsonRequestMixin,
                                       JsonResponseMixin, LimitedTermMixin,
                                       ReAuthenticationRequiredMixin,
                                       # RedirectToDetailMixin,
                                       StaffMemberRequiredMixin,
                                       SuperuserRequiredMixin,
                                       UserAgentMixin, ViewUserKwargsMixin)


class AllowContentTypeNoneView(AllowContentTypeMixin, FormView):
    template_name = "boost/test/index.html"
    form_class = Form
    success_url = '/'


class AllowContentTypeAllowedView(AllowContentTypeMixin, FormView):
    template_name = "boost/test/index.html"
    allowed_content_types = ['text/html']
    form_class = Form
    success_url = '/'


class AllowContentTypeView(AllowContentTypeMixin, FormView):
    template_name = "boost/test/index.html"
    form_class = Form
    success_url = '/'


class CSRFExemptView(CSRFExemptMixin, FormView):
    template_name = "boost/test/index.html"
    form_class = Form
    success_url = '/'


class DynamicRedirectView(DynamicRedirectMixin, FormView):
    template_name = "boost/test/index.html"
    form_class = Form
    success_url = '/'


class JsonRequestView(JsonRequestMixin, FormView):
    template_name = "boost/test/index.html"
    form_class = Form
    success_url = '/'


class JsonResponseView(JsonResponseMixin, View):
    extra_context = {'json': True}


class LimitedTermView(LimitedTermMixin, TemplateView):
    template_name = "boost/test/index.html"


class LimitedTermAfterEndView(LimitedTermMixin, TemplateView):
    template_name = "boost/test/index.html"
    end_datetime = now() - timedelta(days=1)


class LimitedTermBeforeEndView(LimitedTermMixin, TemplateView):
    template_name = "boost/test/index.html"
    end_datetime = now() + timedelta(days=1)


class LimitedTermAfterStartView(LimitedTermMixin, TemplateView):
    template_name = "boost/test/index.html"
    start_datetime = now() - timedelta(days=1)


class LimitedTermBeforeStartView(LimitedTermMixin, TemplateView):
    template_name = "boost/test/index.html"
    start_datetime = now() + timedelta(days=1)


class ReAuthenticationRequiredView(ReAuthenticationRequiredMixin,
                                   TemplateView):
    template_name = "boost/test/index.html"
    interval = 100


class StaffMemberRequiredView(StaffMemberRequiredMixin, TemplateView):
    template_name = "boost/test/index.html"


class SuperuserRequiredView(SuperuserRequiredMixin, TemplateView):
    template_name = "boost/test/index.html"


class UserAgentView(UserAgentMixin, BoostTemplateView):
    template_name = "boost/test/index.html"


class ViewUserKwargsView(ViewUserKwargsMixin, FormView):
    class UserKwargsForm(FormUserKwargsMixin, Form):
        pass
    template_name = "boost/test/index.html"
    form_class = UserKwargsForm
    success_url = '/'
