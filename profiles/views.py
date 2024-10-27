from django.shortcuts import get_object_or_404, render
from accounts.models import FoodieProfile, User
from favorites.models import Favorite
from reviews.models import Review
from timeline.models import Post

def profile_posts(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user)
    return render(request, 'profile_posts.html', {'user': user, 'posts': posts})

def profile_reviews(request, username):
    user = get_object_or_404(User, username=username)
    reviews = Review.objects.filter(user=user)
    return render(request, 'profile_reviews.html', {'user': user, 'reviews': reviews})

def profile_favorites(request, username):
    user = get_object_or_404(User, username=username)
    favorites = Favorite.objects.filter(foodie=user)
    return render(request, 'profile_favorite.html', {'user': user, 'favorites': favorites})

