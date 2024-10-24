from django.urls import path
from .views import *
from . import views

app_name = 'products'

urlpatterns = [
    path('', main, name='main'), # all products
    path('me/', view_products, name='view_products'),
    path('me/<uuid:id>', views.view_product, name='view_product'), # 1 product
    path('me/create-product', create_product, name='create_product'),
    path('me/<uuid:id>/edit-product/', edit_product, name='edit_product'),
    path('me/<uuid:id>/delete/', delete_product, name='delete_product'),
]
