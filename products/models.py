import uuid
from django.db import models
from accounts.models import User

# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=50)
    restaurant = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    category = models.CharField(max_length=30)
    product_image = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.user and hasattr(self.user, 'merchantprofile'):
            self.restaurant = self.user.merchantprofile.restaurant_name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name