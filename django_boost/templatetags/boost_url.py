from urllib import parse

from django.template import Library


register = Library()


@register.filter(name="urlencode", is_safe=True)
def urlencode(value, arg="/"):
    return parse.quote(value, safe=arg)


@register.filter(name="urldecode", is_safe=True)
def urldecode(value):
    return parse.unquote(value)


@register.simple_tag
def replace_parameters(request, *args):
    arg_len = len(args)
    if arg_len % 2 != 0:
        raise LookupError(
            "The number of arguments must be odd, but %s was given" % arg_len)
    url_dict = request.GET.copy()
    for i in range(0, arg_len, 2):
        url_dict[args[i]] = str(args[i + 1])
    return url_dict.urlencode()


@register.simple_tag
def get_querystring(request, value):
    return request.GET.get(value, None)
