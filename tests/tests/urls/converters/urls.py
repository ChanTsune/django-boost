from django.urls import path

from django_boost.urls import register_boost_converters
from django_boost.urls.converters import BOOST_CONVERTERS

from . import views

register_boost_converters()

urlpatterns = [
    path('{x}/<{x}:{x}>'.format(x=x),
         views.EmptyView.as_view(),
         name='{x}'.format(x=x)) for x in BOOST_CONVERTERS.keys()
]
