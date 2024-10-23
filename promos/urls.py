from django.urls import path
from .views import *

app_name = 'promos'

urlpatterns = [
    path('ajax/get_user_products/', views.get_user_products, name='get_user_products'),
    path('promo/create/', views.create_promo, name='create_promo'),  # Untuk form promo
]