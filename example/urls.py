from django.urls import path, include
from . import views
from .views import blog as view_blog

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('reauth/', views.ReloginView.as_view(), name="reauth"),
    path('customer/<int:pk>/detail/',
         views.CustomerDetailView.as_view(), name='customer_detail'),
    path('customer/<int:pk>/update/',
         views.CustomerUpdateView.as_view(), name='customer_update'),
    path('json/', views.JsonView.as_view(extra_context={"json": True})),
    path('json/2/',
         views.JsonView.as_view(extra_context={"json": True}, strictly=True)),
    path('json/post/', views.JsonSampleView.as_view()),
    path('start/', views.StartLimitView.as_view()),
    path('end/', views.EndLimitView.as_view()),
    path('se/', views.SELimitView.as_view()),
    path('views/', include(views.CustomerViews().urls)),
    path('swich/', views.SwichView.as_view(), name="swich_by_user_agent"),
    path('blog/article/', view_blog.ArticleListView.as_view(), name="article_list"),
    path('blog/article/create/',
         view_blog.ArticleCreate.as_view(), name="article_create"),
    path('blog/article/<uuid:pk>/',
         view_blog.ArticleDetail.as_view(), name="article_detail"),
    path('blog/article/<uuid:pk>/update/',
         view_blog.ArticleUpdate.as_view(), name="article_update"),
    path('blog/article/<uuid:pk>/delete/',
         view_blog.ArticleDelete.as_view(), name="article_delete"),
]
