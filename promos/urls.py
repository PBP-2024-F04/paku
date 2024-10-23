from django.urls import path
from .views import *

app_name = 'promos'

urlpatterns = [
    path('promos/', main, name='main'),
    path('promos/add/', add_promo, name='add_promo'),
]