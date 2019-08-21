from django.urls import path, include
from django_boost.urls import UrlSet

from . import views


class JsonSampleUrlSet(UrlSet):
    app_name = 'json'
    urlpatterns = [
        path('', views.JsonView.as_view(extra_context={"json": True})),
        path('2/',
             views.JsonView.as_view(extra_context={"json": True}, strictly=True)),
        path('post/', views.JsonSampleView.as_view()),
    ]

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('reauth/', views.ReloginView.as_view(), name="reauth"),
    path('customer/<int:pk>/detail/',
         views.CustomerDetailView.as_view(), name='customer_detail'),
    path('customer/<int:pk>/update/',
         views.CustomerUpdateView.as_view(), name='customer_update'),
    path('json/', include(JsonSampleUrlSet)),
    path('start/', views.StartLimitView.as_view()),
    path('end/', views.EndLimitView.as_view()),
    path('se/', views.SELimitView.as_view()),
    path('views/', include(views.CustomerViews().urls)),
    path('swich/', views.SwichView.as_view(), name=""),
]
