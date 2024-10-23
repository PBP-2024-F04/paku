from django.db import models
from accounts.models import User

class Post(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.TextField()
