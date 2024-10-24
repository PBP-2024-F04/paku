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

    path('post/<uuid:post_id>/show_comments', get_comments, name='get_comments'),
    path('post/<uuid:post_id>/create_comment', create_comment, name='create_comment'),
]
