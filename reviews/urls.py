from django.urls import path
from .views import *

app_name = 'reviews'

urlpatterns = [
    path('', main, name='main'),
    path('product/<int:product_id>/reviews/', product_reviews, name='product_reviews'),
    path('product/<int:product_id>/reviews/create/', create_review, name='create_review'),
    path('reviews/me/<int:review_id>/edit/', edit_review, name='edit_review'),
    path('reviews/me/<int:review_id>/delete/', delete_review, name='delete_review'),
]
