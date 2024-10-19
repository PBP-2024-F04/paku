from django.urls import path
from .views import main

app_name = 'products'

urlpatterns = [
    path('', main, name='main')
]
