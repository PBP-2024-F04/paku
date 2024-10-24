import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.models import User
from products.models import Product

# Create your models here.
class Promo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    promo_title = models.CharField(max_length=50)
    promo_description = models.CharField(max_length=200)
    batas_penggunaan = models.CharField(max_length=50, default="Tidak ada batas")
    
    @property
    def restaurant_name(self):
        if hasattr(self.user, 'merchantprofile'):
            return self.user.merchantprofile.restaurant_name
        return 'User Invalid'

    def __str__(self):
        return f"{self.promo_title} - {self.product.name}"