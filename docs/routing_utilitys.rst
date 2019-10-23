Routing Utilitys
=================

:synopsis: urlset


UrlSet
-------

If URLs corresponding to multiple models are described in one ``urls.py``, it may be redundant as below.

::

  from django.urls import path
  from . import views

  urlpatterns = [
      path('modelA/', views.ModelAListView.as_view(), name='modelA_list'),
      path('modelA/create/', views.ModelACreateView.as_view(), name='modelA_create'),
      path('modelA/<int:pk>/', views.ModelADetailView.as_view(), name='modelA_detail'),
      path('modelA/<int:pk>/update/', views.ModelAUpdateView.as_view(), name='modelA_update'),
      path('modelA/<int:pk>/delete/', views.ModelADeleteView.as_view(), name='modelA_delete'),
      path('modelB/', views.ModelBListView.as_view(), name='modelB_list'),
      path('modelB/create/', views.ModelBCreateView.as_view(), name='modelB_create'),
      path('modelB/<int:pk>/', views.ModelBDetailView.as_view(), name='modelB_detail'),
      path('modelB/<int:pk>/update/', views.ModelBUpdateView.as_view(), name='modelB_update'),
      path('modelB/<int:pk>/delete/', views.ModelBDeleteView.as_view(), name='modelB_delete'),
  ]

Originally it would be desirable to split the file, but doing so can lead to poor code outlook, due to the increase in files.

In such cases, you can use ``UrlSet``.

When the above code is rewritten using ``UrlSet``, it becomes as follows.

::

  from django.urls import path, include
  from django_boost.urls import UrlSet

  from . import views

  class ModelAUrlSet(UrlSet):
      app_name = "ModelA"
      urlpatterns = [
          path('', views.ModelAListView.as_view(), name='list'),
          path('create/', views.ModelACreateView.as_view(), name='create'),
          path('<int:pk>/', views.ModelADetailView.as_view(), name='detail'),
          path('<int:pk>/update/', views.ModelAUpdateView.as_view(), name='update'),
          path('<int:pk>/delete/', views.ModelADeleteView.as_view(), name='delete'),
      ]

  class ModelBUrlSet(UrlSet):
      app_name = "ModelB"
      urlpatterns = [
          path('', views.ModelBListView.as_view(), name='list'),
          path('create/', views.ModelBCreateView.as_view(), name='create'),
          path('<int:pk>/', views.ModelBDetailView.as_view(), name='detail'),
          path('<int:pk>/update/', views.ModelBUpdateView.as_view(), name='update'),
          path('<int:pk>/delete/', views.ModelBDeleteView.as_view(), name='delete'),
      ]

  urlpatterns = [
      path('modelA/', include(ModelAUrlSet)),
      path('modelB/', include(ModelBUrlSet)),
  ]

URLs are grouped for easy reading.
