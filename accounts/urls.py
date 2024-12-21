from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('home/', home_page, name='home'),
    path('login/', login_page, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_page, name='register'),
    path('register/foodie/', register_foodie_page, name='register_foodie'),
    path('register/merchant/', register_merchant_page, name='register_merchant'),

    path('auth/login/', login),
    path('auth/register/foodie/', register_foodie),
    path('auth/register/merchant/', register_merchant),
    path('auth/logout/', logout),
    
    path('json/get_user_role/', get_user_role, name='get_user_role')
]
