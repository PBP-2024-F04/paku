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
    path('json/', products_json, name='products_json'),
    path('json/<str:id>/', product_by_id_json, name='product_by_id_json'),
    path('create-product-flutter/', create_product_flutter, name='create_product_flutter'),
    path('my-products-flutter/', my_products_flutter, name='my_products_flutter'),
    path('me/<uuid:id>/edit-product-flutter/', edit_product_flutter, name='edit_product_flutter'),
]
