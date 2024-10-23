from django.urls import path
from products.views import main, create_product

app_name = 'products'

urlpatterns = [
    path('', main, name='main'),
    path('create-product', create_product, name='create_product'),
]
