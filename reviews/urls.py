from django.urls import path
from .views import *

app_name = 'reviews'

urlpatterns = [
    path('', main, name='main'),
    path('product/<uuid:product_id>/reviews/', product_review, name='product_review'),
    path('product/<uuid:product_id>/reviews/create/', create_review, name='create_review'),
    path('reviews/me/<uuid:review_id>/edit/', edit_review, name='edit_review'),
    path('reviews/me/<uuid:review_id>/delete/', delete_review, name='delete_review'),

    path('json/', show_json, name='show_json'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('json-reviews/', get_reviews_flutter, name='get_reviews_flutter'),
    path('json-reviews-me/', get_my_reviews_flutter, name='get_my_reviews_flutter'),
    path('json/product/<uuid:product_id>/reviews/', product_review_json, name='product_review_json'),
    path('json/product/<uuid:product_id>/reviews/create/', create_review_json, name='create_review_json'),
    path('json/reviews/me/<uuid:review_id>/edit/', edit_review_json, name='edit_review_json'),
    path('json/reviews/me/<uuid:review_id>/delete/', delete_review_json, name='delete_review_json'),
]
