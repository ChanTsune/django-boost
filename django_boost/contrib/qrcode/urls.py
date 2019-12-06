from django.urls import path

from . import views

app_name = "qrcode"

urlpatterns = [
    path('generate/', views.QRCodeGenerateView.as_view(), name='generate')
]
