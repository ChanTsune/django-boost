from __future__ import annotations

from django_boost.utils.functions.json import json_to_model, model_to_json
from django_boost.utils.functions.loop import (
    loopfirst,
    loopfirstlast,
    looplast,
)

__all__ = [
    "json_to_model",
    "loopfirst",
    "loopfirstlast",
    "looplast",
    "model_to_json",
]
