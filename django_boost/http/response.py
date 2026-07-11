"""Extensions for Django's ``django.http``."""

from __future__ import annotations

from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden, HttpResponseGone,
                         HttpResponseNotAllowed, HttpResponsePermanentRedirect,
                         HttpResponseRedirect, HttpResponseServerError)
from django.http.response import HttpResponseRedirectBase


class HttpResponseTemporaryRedirect(HttpResponseRedirectBase):  # noqa: D101
    status_code = 307


class HttpResponsePermanentRedirect308(HttpResponseRedirectBase):  # noqa: D101
    status_code = 308


class HttpResponseUnauthorized(HttpResponse):  # noqa: D101
    status_code = 401


class HttpResponsePaymentRequired(HttpResponse):  # noqa: D101
    status_code = 402


class HttpResponseNotAcceptable(HttpResponse):  # noqa: D101
    status_code = 406


class HttpResponseProxyAuthenticationRequired(HttpResponse):  # noqa: D101
    status_code = 407


class HttpResponseRequestTimeout(HttpResponse):  # noqa: D101
    status_code = 408


class HttpResponseConflict(HttpResponse):  # noqa: D101
    status_code = 409


class HttpResponseLengthRequired(HttpResponse):  # noqa: D101
    status_code = 411


class HttpResponsePreconditionFailed(HttpResponse):  # noqa: D101
    status_code = 412


class HttpResponsePayloadTooLarge(HttpResponse):  # noqa: D101
    status_code = 413


class HttpResponseURITooLong(HttpResponse):  # noqa: D101
    status_code = 414


class HttpResponseUnsupportedMediaType(HttpResponse):  # noqa: D101
    status_code = 415


class HttpResponseRangeNotSatisfiable(HttpResponse):  # noqa: D101
    status_code = 416


class HttpResponseExpectationFailed(HttpResponse):  # noqa: D101
    status_code = 417


class HttpResponseImATeapot(HttpResponse):  # noqa: D101
    status_code = 418


class HttpResponseMisdirectedRequest(HttpResponse):  # noqa: D101
    status_code = 421


class HttpResponseUnprocessableEntity(HttpResponse):  # noqa: D101
    status_code = 422


class HttpResponseLocked(HttpResponse):  # noqa: D101
    status_code = 423


class HttpResponseFailedDependency(HttpResponse):  # noqa: D101
    status_code = 424


class HttpResponseTooEarly(HttpResponse):  # noqa: D101
    status_code = 425


class HttpResponseUpgradeRequired(HttpResponse):  # noqa: D101
    status_code = 426


class HttpResponsePreconditionRequired(HttpResponse):  # noqa: D101
    status_code = 428


class HttpResponseTooManyRequests(HttpResponse):  # noqa: D101
    status_code = 429


class HttpResponseRequestHeaderFieldsTooLarge(HttpResponse):  # noqa: D101
    status_code = 431


class HttpResponseUnavailableForLegalReasons(HttpResponse):  # noqa: D101
    status_code = 451


class HttpResponseNotImplemented(HttpResponse):  # noqa: D101
    status_code = 501


class HttpResponseBadGateway(HttpResponse):  # noqa: D101
    status_code = 502


class HttpResponseServiceUnavailable(HttpResponse):  # noqa: D101
    status_code = 503


class HttpResponseGatewayTimeout(HttpResponse):  # noqa: D101
    status_code = 504


class HttpResponseHTTPVersionNotSupported(HttpResponse):  # noqa: D101
    status_code = 505


class HttpResponseVariantAlsoNegotiates(HttpResponse):  # noqa: D101
    status_code = 506


class HttpResponseInsufficientStorage(HttpResponse):  # noqa: D101
    status_code = 507


class HttpResponseLoopDetected(HttpResponse):  # noqa: D101
    status_code = 508


class HttpResponseBandwidthLimitExceeded(HttpResponse):  # noqa: D101
    status_code = 509


class HttpResponseNotExtended(HttpResponse):  # noqa: D101
    status_code = 510


class HttpResponseNetworkAuthenticationRequired(HttpResponse):  # noqa: D101
    status_code = 511


class HttpExceptionBase(Exception):
    """Base exception whose ``response_class`` becomes the raised status's HTTP response."""

    response_class = HttpResponse

    @property
    def status_code(self):  # noqa: D102
        return self.response_class.status_code


class HttpRedirectExceptionBase(HttpExceptionBase):
    """Base for exceptions that carry a redirect target, e.g. ``Http301``."""

    def __init__(self, redirect_to, *args):
        """Store the redirect target as ``self.url``."""
        self.url = redirect_to
        super(HttpRedirectExceptionBase, self).__init__(*args)


class Http301(HttpRedirectExceptionBase):  # noqa: D101
    response_class = HttpResponsePermanentRedirect


class Http302(HttpRedirectExceptionBase):  # noqa: D101
    response_class = HttpResponseRedirect


class Http307(HttpRedirectExceptionBase):  # noqa: D101
    response_class = HttpResponseTemporaryRedirect


class Http308(HttpRedirectExceptionBase):  # noqa: D101
    response_class = HttpResponsePermanentRedirect308


class Http400(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseBadRequest


class Http401(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseUnauthorized


class Http402(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponsePaymentRequired


class Http403(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseForbidden


class Http405(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseNotAllowed

    def __init__(self, permitted_methods=(), *args):
        """Store the allowed HTTP methods as ``self.permitted_methods``."""
        self.permitted_methods = permitted_methods
        super().__init__(*args)


class Http406(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseNotAcceptable


class Http407(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseProxyAuthenticationRequired


class Http408(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseRequestTimeout


class Http409(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseConflict


class Http410(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseGone


class Http411(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseLengthRequired


class Http412(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponsePreconditionFailed


class Http413(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponsePayloadTooLarge


class Http414(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseURITooLong


class Http415(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseUnsupportedMediaType


class Http416(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseRangeNotSatisfiable


class Http417(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseExpectationFailed


class Http418(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseImATeapot


class Http421(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseMisdirectedRequest


class Http422(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseUnprocessableEntity


class Http423(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseLocked


class Http424(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseFailedDependency


class Http425(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseTooEarly


class Http426(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseUpgradeRequired


class Http428(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponsePreconditionRequired


class Http429(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseTooManyRequests


class Http431(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseRequestHeaderFieldsTooLarge


class Http451(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseUnavailableForLegalReasons


class Http500(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseServerError


class Http501(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseNotImplemented


class Http502(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseBadGateway


class Http503(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseServiceUnavailable


class Http504(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseGatewayTimeout


class Http505(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseHTTPVersionNotSupported


class Http506(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseVariantAlsoNegotiates


class Http507(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseInsufficientStorage


class Http508(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseLoopDetected


class Http509(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseBandwidthLimitExceeded


class Http510(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseNotExtended


class Http511(HttpExceptionBase):  # noqa: D101
    response_class = HttpResponseNetworkAuthenticationRequired
