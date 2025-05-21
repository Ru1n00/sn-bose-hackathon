from django.urls import path

from .views import (
    index,
    PostListView,
    post_detail,
)

app_name = 'content'

urlpatterns = [
    path('', index, name='index'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('post/<str:slug>', post_detail, name='post_detail'),
]