from django.urls import path
from .views import *

app_name = 'profiles'

urlpatterns = [
    path('@<str:username>', profile_page, name='profile_page')
]
