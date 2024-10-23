from django.urls import path
from .views import *

app_name = 'favorites'

urlpatterns = [
    path('', main, name='main'),
    path('favorites/create/<uuid:product_id>/', create_favorite, name='create_favorite'),
]
