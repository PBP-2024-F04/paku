from django.urls import path
from .views import *

app_name = 'favorites'

urlpatterns = [
    path('', main, name='main')
]
