from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Favorite
from .forms import FavoriteForm
from accounts.models import User, FoodieProfile

@login_required(login_url='/accounts/login')
def main(request):
    context = {
        'user': request.user,
        'want_to_try': Favorite.objects.filter(foodie=request.user, category='want_to_try'),
        'loving_it': Favorite.objects.filter(foodie=request.user, category='loving_it'),
        'all_time_favorites': Favorite.objects.filter(foodie=request.user, category='all_time_favorites')
    }

    return render(request, 'favorites.html', context)

@login_required(login_url='/accounts/login')
def create_favorite(request, product_id):
    product = Product.objects.get(pk = product_id) 
    form = FavoriteForm(request.POST or None)
        
    if form.is_valid() and request.method == 'POST':
        favorite = form.save(commit=False)
        favorite.foodie = request.user 
        favorite.product = product  
        favorite.save() 
        return redirect('favorites:main')
    
    context = {'form': form, 'product': product}
    return render(request, 'create_favorite.html', context)

def edit_favorite(request, favorite_id):
    favorite = Favorite.objects.get(pk=favorite_id)
    form = FavoriteForm(request.POST or None, instance=favorite)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('favorites:main')

    context = {'form': form}

    return render(request, 'edit_favorite.html', context)

def delete_favorite(request, favorite_id):
    favorite = Product.objects.get(pk = favorite_id) 
    favorite.delete()
    return redirect('favorites:main')

def user_favorites(request, user_id):
    profile_user = User.objects.get(pk = user_id)
    favorites = Favorite.objects.filter(foodie=profile_user)

    # Filter berdasarkan kategori
    want_to_try = favorites.filter(category='want_to_try')
    loving_it = favorites.filter(category='loving_it')
    all_time_favorites = favorites.filter(category='all_time_favorites')

    context = {
        'profile_user': profile_user,
        'want_to_try': want_to_try,
        'loving_it': loving_it,
        'all_time_favorites': all_time_favorites,
    }
    return render(request, 'favorites/profile_favorites.html', context)