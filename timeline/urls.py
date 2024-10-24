from django.urls import path
from .views import *

app_name = 'timeline'

urlpatterns = [
    path('', main, name='main'),
    path('post/', create_post, name='create_post'),
    path('post/<uuid:post_id>', view_post, name='view_post'),
    path('post/<uuid:post_id>/edit', edit_post, name='edit_post'),
    path('post/<uuid:post_id>/delete', delete_post, name='delete_post'),

    path('post/<uuid:post_id>/comment', get_comments, name='get_comments'),
    path('post/<uuid:post_id>/comment/create', create_comment, name='create_comment'),

    path('comment/<uuid:comment_id>/edit', edit_comment, name='edit_comment'),
    path('comment/<uuid:comment_id>/delete', delete_comment, name='delete_comment'),
]
