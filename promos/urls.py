from django.urls import path
from .views import *

app_name = 'promos'

urlpatterns = [
    path('', main, name='main')
]