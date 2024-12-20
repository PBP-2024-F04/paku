from django.urls import path
from .views import *

app_name = 'profiles'

urlpatterns = [
    path('@<str:username>', profile_posts, name='profile_posts'),
    path('@<str:username>/reviews', profile_reviews, name='profile_reviews'),
    path('@<str:username>/favorites', profile_favorites, name='profile_favorites'),
    path('@<str:username>/products', profile_products, name='profile_products'),

    path('json/<str:username>', profile_json, name='profile_json'),
    path('json/<str:username>/posts', profile_posts_json, name='profile_posts_json'),
    path('json/<str:username>/reviews', profile_reviews_json, name='profile_reviews_json'),
    path('json/<str:username>/favorites', profile_favorites_json, name='profile_favorites_json'),
    path('json/<str:username>/products', profile_products_json, name='profile_products_json'),
]
