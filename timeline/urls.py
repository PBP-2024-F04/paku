from django.urls import path
from .views import *

app_name = 'timeline'

urlpatterns = [
    path('', main, name='main')
]
