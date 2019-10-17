
def _get_queryset(klass):
    """Return a QuerySet or a Manager."""
    # If it is a model class or anything else with ._default_manager
    if hasattr(klass, '_default_manager'):
        return klass._default_manager.all()
    return klass


def get_object_or_default(klass, *args, default=None, **kwargs):
    """
    Use get() to return an object or return default if the object
    does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.
    Like with QuerySet.get(), MultipleObjectsReturned is raised if more than
    one object is found.
    """
    queryset = _get_queryset(klass)
    if not hasattr(queryset, 'get'):
        klass__name = klass.__name__ if isinstance(
            klass, type) else klass.__class__.__name__
        raise ValueError(
            "First argument to get_object_or_default() must be a Model, "
            "Manager, or QuerySet, not '%s'." % klass__name
        )
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return default


def get_object_or_exception(klass, *args, exception=None, **kwargs):
    """
    Use get() to return an object, or raise exception if the object
    does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.
    Like with QuerySet.get(), MultipleObjectsReturned is raised if more than
    one object is found.
    """
    queryset = _get_queryset(klass)
    if not hasattr(queryset, 'get'):
        klass__name = klass.__name__ if isinstance(
            klass, type) else klass.__class__.__name__
        raise ValueError(
            "First argument to get_object_or_default() must be a Model, "
            "Manager, or QuerySet, not '%s'." % klass__name
        )
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        raise exception


def get_list_or_default(klass, *args, default=None, **kwargs):
    """
    Use filter() to return a list of objects, or return default if
    the list is empty.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the filter() query.
    """
    queryset = _get_queryset(klass)
    if not hasattr(queryset, 'filter'):
        klass__name = klass.__name__ if isinstance(
            klass, type) else klass.__class__.__name__
        raise ValueError(
            "First argument to get_object_or_default() must be a Model, "
            "Manager, or QuerySet, not '%s'." % klass__name
        )
    obj_list = list(queryset.filter(*args, **kwargs))
    if not obj_list:
        return default
    return obj_list


def get_list_or_exception(klass, *args, exception=None, **kwargs):
    """
    Use filter() to return a list of objects, or raise exception if
    the list is empty.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the filter() query.
    """
    queryset = _get_queryset(klass)
    if not hasattr(queryset, 'filter'):
        klass__name = klass.__name__ if isinstance(
            klass, type) else klass.__class__.__name__
        raise ValueError(
            "First argument to get_object_or_default() must be a Model, "
            "Manager, or QuerySet, not '%s'." % klass__name
        )
    obj_list = list(queryset.filter(*args, **kwargs))
    if not obj_list:
        raise exception
    return obj_list
