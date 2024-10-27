import uuid
from django.db import models
from products.models import Product
from accounts.models import User

class Favorite(models.Model):
    class Category(models.TextChoices):
        WANT_TO_TRY = 'want_to_try', 'Want to Try'
        CANT_GET_ENOUGH = 'loving_it', 'Loving It'
        ALL_TIME_FAVORITES = 'all_time_favorites', 'All Time Favorites'

    favorite_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    foodie = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Foodie'})
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=Category.choices)