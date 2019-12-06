from django.core.checks import Error, register

default_app_config = 'django_boost.contrib.qrcode.apps.QrcodeConfig'


@register
def check_modules(app_configs, **kwargs):
    errors = []
    try:
        import qrcode
    except ImportError:
        errors.append(
            Error("qrcode is not installed. please install 'qrcode'.",
                  hint="run command 'python -m pip install qrcode'")
            )
    return errors
