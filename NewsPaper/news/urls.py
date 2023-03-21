from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
    #path('news_list/', index, name='index'),
    path('', PostList.as_view(), name='home'),
    path('news_list/', PostList.as_view(), name='news_list'),
    path('news/<int:id>/', detail, name='post_detail_show'),
    path('news/search/', PostSearch.as_view()),
    path('news/create/', PostCreate.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', PostDetailEdit.as_view(), name='post_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('news/<int:pk>/comment_create/', comment_create_view, name='comment_create'),
    path('articles/<int:id>/', detail, name='post_detail_show_ar'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleDetailEdit.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('articles/<int:pk>/comment_create/', comment_create_view, name='ar_comment_create'),
    path('news/<int:id1>/comment/<int:id2>/edit/', comment_edit_view, name='comment_edit'),
    path('news/<int:id1>/comment/<int:id2>/delete/', comment_delete_view, name='comment_delete'),
    #path('news/<int:id1>/comment/<int:id2>/delete/', CommentDelete.as_view(), name='comment_delete'),
    #path('', IndexView.as_view()), # для экспериментов

]