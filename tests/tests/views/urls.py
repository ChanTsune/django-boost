from django.urls import path

from . import views

urlpatterns = [
    path('', views.StringView.as_view(), name='empty'),
    path('simple/', views.SimpleStringView.as_view(), name='simple'),
    path('dynamic/<int:key1>/<str:key2>/', views.DynamicStringView.as_view(), name='dynamic'),
    path('after/', views.AfterViewProcessView.as_view(), name='after'),
    path('after/short-circuit/', views.ShortCircuitAfterViewProcessView.as_view(), name='after_short_circuit'),
    path('after/generic/', views.GenericAfterViewProcessView.as_view(), name='after_generic'),
]
