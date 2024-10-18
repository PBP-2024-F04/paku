from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        FOODIE = 'Foodie'
        MERCHANT = 'Merchant'

    base_role: Role

    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)

class Foodie(User):
    base_role = User.Role.FOODIE

    class Meta:
        proxy = True

class FoodieProfile(models.Model):
    foodie = models.OneToOneField(Foodie, on_delete=models.CASCADE)

class Merchant(User):
    base_role = User.Role.MERCHANT

    class Meta:
        proxy = True

class MerchantProfile(models.Model):
    merchant = models.OneToOneField(Merchant, on_delete=models.CASCADE)
