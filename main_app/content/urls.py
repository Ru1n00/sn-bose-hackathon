from django.urls import path

from .views import (
    index,
    PostListView,
    post_detail,
    post_create,
    post_edit
)

app_name = 'content'

urlpatterns = [
    path('', index, name='index'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('post/<str:slug>/', post_detail, name='post_detail'),
    path('post-create/', post_create, name='post_create'),
    path('post/<str:slug>/edit/', post_edit, name='post_edit'),
]