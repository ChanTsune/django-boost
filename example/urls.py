from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('reauth/',views.ReloginView.as_view(),name="reauth"),
    path('customer/<int:pk>/detail/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('customer/<int:pk>/update/', views.CustomerUpdateView.as_view(), name='customer_update'),
    path('json/', views.JsonView.as_view(extra_response_data={"json": True})),
    path('json/2/', views.JsonView.as_view(extra_response_data={"json": True}, strictly=True)),
]
