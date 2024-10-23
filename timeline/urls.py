from django.urls import path
from .views import *

app_name = 'timeline'

urlpatterns = [
    path('', main, name='main'),
    path('create/', create_post, name='create_post'),
    path('view/<uuid:post_id>', view_post, name='view_post'),
    path('edit/<uuid:post_id>', edit_post, name='edit_post'),
    path('delete/<uuid:post_id>', delete_post, name='delete_post'),
]
