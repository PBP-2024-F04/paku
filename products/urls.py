from django.urls import path
from .views import *
from . import views

app_name = 'products'

urlpatterns = [
    path('', main, name='main'),
    path('me/', my_products, name='my_products'),
    path('me/<uuid:id>/', view_product, name='view_product'),
    path('me/create-product/', create_product, name='create_product'),
    path('me/<uuid:id>/edit-product/', edit_product, name='edit_product'),
    path('me/<uuid:id>/delete-product/', delete_product, name='delete_product'),
    path('json/', show_json, name='show_json'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('create-product-flutter/', create_product_flutter, name='create_product_flutter'),
]
