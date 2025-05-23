from django.urls import path

from .views import (
    index,
    PostListView,
    post_detail,
    post_create,
    post_edit,
    CategoryPostListView,
    PostSearchView,
    make_comment,
    post_upvote,
    post_downvote,
)

app_name = 'content'

urlpatterns = [
    path('', index, name='index'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<str:category_slug>/', CategoryPostListView.as_view(), name='category_post_list'),
    path('post/<str:slug>/', post_detail, name='post_detail'),
    path('post-create/', post_create, name='post_create'),
    path('post/<str:slug>/edit/', post_edit, name='post_edit'),
    path('post/<str:slug>/upvote/', post_upvote, name='post_upvote'),
    path('post/<str:slug>/downvote/', post_downvote, name='post_downvote'),
    path('make-comment/', make_comment, name='make_comment'),
    path('search/', PostSearchView.as_view(), name='search'),
]