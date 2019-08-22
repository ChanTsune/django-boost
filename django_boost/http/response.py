from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden, HttpResponseGone,
                         HttpResponseNotAllowed, HttpResponsePermanentRedirect,
                         HttpResponseRedirect, HttpResponseServerError)
from django.http.response import HttpResponseRedirectBase


class HttpResponseTemporaryRedirect(HttpResponseRedirectBase):
    status_code = 307


class HttpResponsePermanentRedirect308(HttpResponseRedirectBase):
    status_code = 308


class HttpResponseUnauthorized(HttpResponse):
    status_code = 401


class HttpResponsePaymentRequired(HttpResponse):
    status_code = 402


class HttpResponseNotAcceptable(HttpResponse):
    status_code = 406


class HttpResponseProxyAuthenticationRequired(HttpResponse):
    status_code = 407


class HttpResponseRequestTimeout(HttpResponse):
    status_code = 408


class HttpResponseConflict(HttpResponse):
    status_code = 409


class HttpResponseLengthRequired(HttpResponse):
    status_code = 411


class HttpResponsePreconditionFailed(HttpResponse):
    status_code = 412


class HttpResponsePayloadTooLarge(HttpResponse):
    status_code = 413


class HttpResponseURITooLong(HttpResponse):
    status_code = 414


class HttpResponseUnsupportedMediaType(HttpResponse):
    status_code = 415


class HttpResponseRangeNotSatisfiable(HttpResponse):
    status_code = 416


class HttpResponseExpectationFailed(HttpResponse):
    status_code = 417


class HttpResponseImATeapot(HttpResponse):
    status_code = 418


class HttpResponseMisdirectedRequest(HttpResponse):
    status_code = 421


class HttpResponseUnprocessableEntity(HttpResponse):
    status_code = 422


class HttpResponseLocked(HttpResponse):
    status_code = 423


class HttpResponseFailedDependency(HttpResponse):
    status_code = 424


class HttpResponseTooEarly(HttpResponse):
    status_code = 425


class HttpResponseUpgradeRequired(HttpResponse):
    status_code = 426


class HttpResponsePreconditionRequired(HttpResponse):
    status_code = 428


class HttpResponseTooManyRequests(HttpResponse):
    status_code = 429


class HttpResponseRequestHeaderFieldsTooLarge(HttpResponse):
    status_code = 431


class HttpResponseUnavailableForLegalReasons(HttpResponse):
    status_code = 451


class HttpResponseNotImplemented(HttpResponse):
    status_code = 501


class HttpResponseBadGateway(HttpResponse):
    status_code = 502


class HttpResponseServiceUnavailable(HttpResponse):
    status_code = 503


class HttpResponseGatewayTimeout(HttpResponse):
    status_code = 504


class HttpResponseHTTPVersionNotSupported(HttpResponse):
    status_code = 505


class HttpResponseVariantAlsoNegotiates(HttpResponse):
    status_code = 506


class HttpResponseInsufficientStorage(HttpResponse):
    status_code = 507


class HttpResponseLoopDetected(HttpResponse):
    status_code = 508


class HttpResponseBandwidthLimitExceeded(HttpResponse):
    status_code = 509


class HttpResponseNotExtended(HttpResponse):
    status_code = 510


class HttpResponseNetworkAuthenticationRequired(HttpResponse):
    status_code = 511


class HttpExceptionBase(Exception):
    response_class = HttpResponse

    @property
    def status_code(self):
        return self.response_class.status_code


class HttpRedirectExceptionBase(HttpExceptionBase):

    def __init__(self, redirect_to, *args):
        self.url = redirect_to
        super(HttpRedirectExceptionBase, self).__init__(*args)


class Http301(HttpRedirectExceptionBase):
    response_class = HttpResponsePermanentRedirect


class Http302(HttpRedirectExceptionBase):
    response_class = HttpResponseRedirect


class Http307(HttpRedirectExceptionBase):
    response_class = HttpResponseTemporaryRedirect


class Http308(HttpRedirectExceptionBase):
    response_class = HttpResponsePermanentRedirect308


class Http400(HttpExceptionBase):
    response_class = HttpResponseBadRequest


class Http401(HttpExceptionBase):
    response_class = HttpResponseUnauthorized


class Http402(HttpExceptionBase):
    response_class = HttpResponsePaymentRequired


class Http403(HttpExceptionBase):
    response_class = HttpResponseForbidden


class Http405(HttpExceptionBase):
    response_class = HttpResponseNotAllowed


class Http406(HttpExceptionBase):
    response_class = HttpResponseNotAcceptable


class Http407(HttpExceptionBase):
    response_class = HttpResponseProxyAuthenticationRequired


class Http408(HttpExceptionBase):
    response_class = HttpResponseRequestTimeout


class Http409(HttpExceptionBase):
    response_class = HttpResponseConflict


class Http410(HttpExceptionBase):
    response_class = HttpResponseGone


class Http411(HttpExceptionBase):
    response_class = HttpResponseLengthRequired


class Http412(HttpExceptionBase):
    response_class = HttpResponsePreconditionFailed


class Http413(HttpExceptionBase):
    response_class = HttpResponsePayloadTooLarge


class Http414(HttpExceptionBase):
    response_class = HttpResponseURITooLong


class Http415(HttpExceptionBase):
    response_class = HttpResponseUnsupportedMediaType


class Http416(HttpExceptionBase):
    response_class = HttpResponseRangeNotSatisfiable


class Http417(HttpExceptionBase):
    response_class = HttpResponseExpectationFailed


class Http418(HttpExceptionBase):
    response_class = HttpResponseImATeapot


class Http421(HttpExceptionBase):
    response_class = HttpResponseMisdirectedRequest


class Http422(HttpExceptionBase):
    response_class = HttpResponseUnprocessableEntity


class Http423(HttpExceptionBase):
    response_class = HttpResponseLocked


class Http424(HttpExceptionBase):
    response_class = HttpResponseFailedDependency


class Http425(HttpExceptionBase):
    response_class = HttpResponseTooEarly


class Http426(HttpExceptionBase):
    response_class = HttpResponseUpgradeRequired


class Http428(HttpExceptionBase):
    response_class = HttpResponsePreconditionRequired


class Http429(HttpExceptionBase):
    response_class = HttpResponseTooManyRequests


class Http431(HttpExceptionBase):
    response_class = HttpResponseRequestHeaderFieldsTooLarge


class Http451(HttpExceptionBase):
    response_class = HttpResponseUnavailableForLegalReasons


class Http500(HttpExceptionBase):
    response_class = HttpResponseServerError


class Http501(HttpExceptionBase):
    response_class = HttpResponseNotImplemented


class Http502(HttpExceptionBase):
    response_class = HttpResponseBadGateway


class Http503(HttpExceptionBase):
    response_class = HttpResponseServiceUnavailable


class Http504(HttpExceptionBase):
    response_class = HttpResponseGatewayTimeout


class Http507(HttpExceptionBase):
    response_class = HttpResponseInsufficientStorage
