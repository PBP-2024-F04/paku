from django.db import models
from accounts.models import User
from uuid import uuid4

class Post(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
