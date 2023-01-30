from django.urls import path
from .views import *

urlpatterns = [
    #path('news_list/', index, name='index'),
    path('', PostList.as_view()),
    path('news_list/', PostList.as_view()),
    path('news/<int:id>', detail, name='detail'),
    path('news/<int:pk>/edit/', PostDetailEdit.as_view(), name='post_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('news/create/', PostCreate.as_view(), name='post_creating'),
    path('articles/create/', ArticleCreate.as_view(), name='article_creating'),
    path('articles/<int:pk>/edit/', PostDetailEdit.as_view(), name='post_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

]