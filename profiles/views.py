from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from accounts.models import FoodieProfile, MerchantProfile, User
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

def my_profile_json(request):
    user = request.user

    return JsonResponse({
        'username': user.username,
        'display_name':
            user.foodieprofile.full_name
            if user.role == "Foodie"
            else user.merchantprofile.restaurant_name,
        'role': user.role,
    }, safe=False)

def profile_json(_, username):
    user = get_object_or_404(User, username=username)

    display_name = \
        FoodieProfile.objects.get(user=user).full_name \
        if user.role == "Foodie" else \
        MerchantProfile.objects.get(user=user).restaurant_name

    return JsonResponse({
        'username': user.username,
        'display_name': display_name,
        'role': user.role,
    }, safe=False)

def profile_posts_json(_, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user)

    data = [
        {
            "id": post.id,
            "user": {
                "role": post.user.role,
                "display_name":
                    post.user.foodieprofile.full_name
                    if post.user.role == "Foodie" else
                    post.user.merchantprofile.restaurant_name,
                "username": post.user.username,
            },
            "text": post.text,
            "is_edited": post.is_edited,
            "is_mine": True,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
        }
        for post in posts
    ]

    return JsonResponse(data, content_type="application/json", safe=False)

def profile_reviews_json(request, username):
    return JsonResponse({})

def profile_favorites_json(request, username):
    return JsonResponse({})

def profile_products_json(request, username):
    return JsonResponse({})
