from django.db import models


def model_to_json(model, fields=(), exclude=()):
    """
    Take Model or Model.QuerySet as an argument.

    Return value is a dictionary or a list for dictionary.
    """
    if isinstance(model, models.Model):
        json_data = {}

        if fields:
            for f in fields:
                json_data[f] = getattr(model, f)
            return json_data

        elif exclude:
            for f in model._meta.fields:
                if f.name not in exclude:
                    json_data[f.name] = getattr(model, f.name)
            return json_data

        else:
            for f in model._meta.fields:
                json_data[f.name] = getattr(model, f.name)
            return json_data

    elif isinstance(model, models.QuerySet):
        json_data = [model_to_json(m, fields, exclude) for m in model]
        return json_data

    raise TypeError('argument must be {} or {}'.format(
        models.Model, models.QuerySet))


def json_to_model(model_class, dic, fields=(), exclude=()):
    model = model_class()
    if fields:
        for key, value in dic.items():
            if key in fields:
                setattr(model, key, value)
        return model

    elif exclude:
        for key, value in dic.items():
            if key not in exclude:
                setattr(model, key, value)
        return model

    for key, value in dic.items():
        setattr(model, key, value)
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
