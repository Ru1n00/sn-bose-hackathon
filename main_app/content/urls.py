from django.urls import path

from .views import (
    index,
    PostListView,
)

app_name = 'content'

urlpatterns = [
    path('', index, name='index'),
    path('posts/', PostListView.as_view(), name='post_list'),
]