from django.urls import path
from .views import main, my_promos, add_promo, update_promo, delete_promo, promo_list_json, my_promo_list_json, create_promo_json, edit_promo_json, delete_promo_json

app_name = 'promos'

urlpatterns = [
    path('', main, name='main'),
    path('my_promos/', my_promos, name='my_promos'),
    path('add_promo/', add_promo, name='add_promo'),
    path('update_promo/<uuid:promo_id>/', update_promo, name='update_promo'),
    path('delete_promo/<uuid:promo_id>/', delete_promo, name='delete_promo'),
    path('promo_list_json/', promo_list_json, name='promo_list_json'),
    path('my_promo_list_json/', my_promo_list_json, name='my_promo_list_json'),
    path('create_promo_json/', create_promo_json, name='create_promo_json'),
     path('edit_promo_json/<uuid:promo_id>/', edit_promo_json, name='edit_promo_json'),
    path('delete_promo_json/<uuid:promo_id>/', delete_promo_json, name='delete_promo_json'),
]