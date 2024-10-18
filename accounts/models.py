from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    class Role(models.TextChoices):
        FOODIE = 'Foodie'
        MERCHANT = 'Merchant'

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.FOODIE)

@receiver(post_save, sender=User)
def autocreate_profile(sender, instance: User, created, **kwargs):
    if created:
        match instance.role:
            case User.Role.FOODIE:
                FoodieProfile.objects.create(user=instance)
            case User.Role.MERCHANT:
                MerchantProfile.objects.create(user=instance)

class FoodieProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class MerchantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
