from django.urls import path
from .views import *

urlpatterns = [
    #path('news_list/', index, name='index'),
    path('', PostList.as_view(), name='home'),
    path('news_list/', PostList.as_view(), name='news_list'),
    path('news/<int:id>', detail, name='detail'),
    path('news/search/', PostSearch.as_view()),
    path('news/create/', PostCreate.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', PostDetailEdit.as_view(), name='post_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('articles/<int:id>', detail, name='detail_ar'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleDetailEdit.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]