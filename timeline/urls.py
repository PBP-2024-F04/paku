from django.urls import path
from .views import *

app_name = 'timeline'

urlpatterns = [
    path('', main, name='main'),
    path('post/', create_post, name='create_post'),
    path('post/<uuid:post_id>', view_post, name='view_post'),
    path('post/<uuid:post_id>/edit', edit_post, name='edit_post'),
    path('post/<uuid:post_id>/delete', delete_post, name='delete_post'),

    path('comment/<uuid:comment_id>/edit', edit_comment, name='edit_comment'),
    path('comment/<uuid:comment_id>/delete', delete_comment, name='delete_comment'),

    path('json/posts', get_posts_json, name='get_posts_json'),
    path('json/posts/create', create_post_json, name='create_post_json'),
    path('json/posts/<uuid:post_id>/edit', edit_post_json, name='edit_post_json'),
    path('json/posts/<uuid:post_id>/delete', delete_post_json, name='delete_post_json'),
    path('json/posts/<uuid:post_id>/comments', get_comments_json, name='get_comments_json'),
    path('json/posts/<uuid:post_id>/comments/create', create_comment_json, name='create_comment_json'),

    path('json/comments/<uuid:comment_id>/edit', edit_comment_json, name='edit_comment_json'),
    path('json/comments/<uuid:comment_id>/delete', delete_comment_json, name='delete_comment_json'),
]
