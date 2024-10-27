from django.shortcuts import get_object_or_404, render

from accounts.models import User
from timeline.models import Post

def profile_posts(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user)
    return render(request, 'profile_posts.html', {'user': user, 'posts': posts})

