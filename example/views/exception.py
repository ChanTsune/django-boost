from __future__ import annotations

from typing import Any, NoReturn

from django_boost.views.generic import TemplateView
from django_boost.http.response import Http415


class E415View(TemplateView):

    def get_context_data(self, **kwargs: Any) -> NoReturn:
        raise Http415
