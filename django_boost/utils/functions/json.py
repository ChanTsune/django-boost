"""Model/JSON conversion helpers."""

from __future__ import annotations

from collections.abc import Collection, Mapping
from typing import Any, TypeVar, overload

from django.db import models

__all__ = ["json_to_model", "model_to_json"]

_M = TypeVar("_M", bound=models.Model)


@overload
def model_to_json(
    model: models.Model,
    fields: Collection[str] = ...,
    exclude: Collection[str] = ...,
) -> dict[str, Any]: ...


@overload
def model_to_json(
    model: models.QuerySet[models.Model],
    fields: Collection[str] = ...,
    exclude: Collection[str] = ...,
) -> list[dict[str, Any]]: ...


def model_to_json(
    model: models.Model | models.QuerySet[models.Model],
    fields: Collection[str] = (),
    exclude: Collection[str] = (),
) -> dict[str, Any] | list[dict[str, Any]]:
    """
    Take Model or Model.QuerySet as an argument.

    Return value is a dictionary or a list for dictionary.
    """
    if isinstance(model, models.Model):
        opts = model._meta
        json_data: dict[str, Any] = {}
        for f in opts.fields:
            if fields and f.name not in fields:
                continue
            if exclude and f.name in exclude:
                continue
            json_data[f.name] = f.value_from_object(model)
        return json_data

    elif isinstance(model, models.QuerySet):
        return [model_to_json(m, fields, exclude) for m in model]

    raise TypeError(
        'model_to_json() argument must be a Model or QuerySet, not %s'
        % type(model).__name__
    )


def json_to_model(
    model_class: type[_M],
    dic: Mapping[str, Any],
    fields: Collection[str] = (),
    exclude: Collection[str] = (),
) -> _M:
    """Build an unsaved ``model_class`` instance from a dict shaped like ``model_to_json``'s output."""
    model = model_class()
    for f in model._meta.fields:
        if fields and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        # Assign via attname so relation fields receive the stored pk on their
        # *_id column; for plain fields name == attname. model_to_json keys the
        # value by f.name but stores value_from_object (the attname value).
        setattr(model, f.attname, dic[f.name])
    return model
