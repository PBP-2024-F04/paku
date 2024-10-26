from django.urls import path
from .views import *

app_name = 'favorites'

urlpatterns = [
    path('', main, name='main'),
    path('create/<uuid:product_id>/', create_favorite, name='create_favorite'),
    path('<uuid:favorite_id>/edit', edit_favorite, name='edit_favorite'),
    path('<uuid:favorite_id>/delete', delete_favorite, name='delete_favorite'),
    path('category/<str:category_name>', category_favorites, name='category_favorites'), 
]
