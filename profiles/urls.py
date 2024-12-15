from django.urls import path
from .views import *

app_name = 'profiles'

urlpatterns = [
    path('@<str:username>', profile_posts, name='profile_posts'),
    path('@<str:username>/reviews', profile_reviews, name='profile_reviews'),
    path('@<str:username>/favorites', profile_favorites, name='profile_favorites'),
    path('@<str:username>/products', profile_products, name='profile_products'),
]
