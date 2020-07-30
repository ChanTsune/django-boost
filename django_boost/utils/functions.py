from django.db import models


def model_to_json(model, fields=(), exclude=()):
    """
    Take Model or Model.QuerySet as an argument.

    Return value is a dictionary or a list for dictionary.
    """
    opts = model._meta
    if isinstance(model, models.Model):
        json_data = {}
        for f in opts.fields:
            if fields and f.name not in fields:
                continue
            if exclude and f.name in exclude:
                continue
            json_data[f.name] = f.value_from_object(model)
        return json_data

    elif isinstance(model, models.QuerySet):
        json_data = [model_to_json(m, fields, exclude) for m in model]
        return json_data

    raise TypeError('argument must be {} or {}'.format(
        models.Model, models.QuerySet))


def json_to_model(model_class, dic, fields=(), exclude=()):
    model = model_class()
    for f in model._meta.fields:
        if fields and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        setattr(model, f.name, dic[f.name])
    return model


def loopfirst(iterable):
    """
    Loop util.

    Yield True when the first element of the given iterator object,
    False otherwise.
    """
    it = iter(iterable)
    for i, val in enumerate(it):
        yield i == 0, val


def looplast(iterable):
    """
    Loop util.

    Yield True when the last element of the given iterator object,
    False otherwise.
    """
    it = iterable
    last_index = len(it) - 1
    for i, val in enumerate(it):
        yield i == last_index, val


def loopfirstlast(iterable):
    """
    A function combining `firstloop` and` lastloop`.

    Yield True if the first and last element of the iterator object,
    False otherwise.
    """
    it = iterable
    last_index = len(it) - 1
    for i, val in enumerate(it):
        yield i == 0 or i == last_index, val
