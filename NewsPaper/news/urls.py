from django.urls import path
from .views import index, detail

urlpatterns = [
    path('news_list/', index, name='index'),
    path('new/<int:id>', detail, name='detail'),
]