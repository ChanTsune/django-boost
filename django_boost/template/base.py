"""Extensions for Django's ``django.template``."""

from __future__ import annotations


class StrictInvalidTemplateVariable(str):
    """
    Raise an exception when Django renders an invalid template variable.

    Intended for Django's ``string_if_invalid`` template engine option.

    The instance value is ``'%s'`` on purpose. Django renders an invalid
    variable as ``string_if_invalid % var`` only when ``'%s' in
    string_if_invalid``; carrying exactly that value routes resolution through
    ``__mod__``, where this class raises instead of substituting. An empty or
    ``%s``-free value would silently disable the hook.
    """

    default_message = "Template variable or property '{name}' is invalid or missing."

    def __new__(cls, message=None, exception_class=ValueError):
        if not (isinstance(exception_class, type) and issubclass(exception_class, Exception)):
            raise TypeError("exception_class must be an Exception subclass, "
                            "got %r." % (exception_class,))
        message = cls.default_message if message is None else message
        # Validate the template at construction time so an unknown or stray
        # placeholder fails where the option is configured, rather than masking
        # the invalid-variable error with a KeyError/IndexError during render.
        try:
            message.format(name="")
        except (KeyError, IndexError, ValueError) as exc:
            raise ValueError("message may only reference the {name} "
                             "placeholder: %s" % exc)
        obj = super().__new__(cls, '%s')
        obj.message = message
        obj.exception_class = exception_class
        return obj

    def __mod__(self, missing):  # noqa: D105
        raise self.exception_class(self.message.format(name=missing))
