from django.urls import path
from .views import *

app_name = 'products'

urlpatterns = [
    path('products/', main, name='main'),
    path('products/create-product', create_product, name='create_product'),
    path('products/edit-product/<uuid:id>', edit_product, name='edit_product'),
    path('products/delete/<uuid:id>', delete_product, name='delete_product'),
]
