from django.urls import path

from . import views

urlpatterns = [
    path('', views.StringView.as_view(), name='empty'),
    path('simple/', views.SimpleStringView.as_view(), name='simple'),
    path('dynamic/<int:key1>/<str:key2>/', views.DynamicStringView.as_view(), name='dynamic'),
]
