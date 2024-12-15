from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from accounts.models import User
from favorites.models import Favorite
from products.models import Product
from reviews.models import Review
from timeline.models import Post

@login_required(login_url='/accounts/login')
def profile_posts(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user)
    return render(request, 'profile_posts.html', {'user': user, 'posts': posts})

@login_required(login_url='/accounts/login')
def profile_reviews(request, username):
    user = get_object_or_404(User, username=username)
    reviews = Review.objects.filter(user=user)
    return render(request, 'profile_reviews.html', {'user': user, 'reviews': reviews})

@login_required(login_url='/accounts/login')
def profile_favorites(request, username):
    user = get_object_or_404(User, username=username)
    favorites = Favorite.objects.filter(foodie=user)
    return render(request, 'profile_favorite.html', {'user': user, 'favorites': favorites})

@login_required(login_url='/accounts/login')
def profile_products(request, username):
    user = get_object_or_404(User, username=username)
    products = Product.objects.filter(user=user)
    return render(request, 'profile_products.html', {'user': user, 'products': products})
