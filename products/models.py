from django.db import models
import uuid
from accounts.models import User

# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=255)
    restaurant = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    category = models.CharField(max_length=255)