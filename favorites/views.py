from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from products.models import Product
from .models import Favorite
from .forms import FavoriteForm
from accounts.models import User, FoodieProfile

def main(request):
    context = {
        'user': request.user,
        'want_to_try': Favorite.objects.filter(foodie=request.user, category='want_to_try'),
        'loving_it': Favorite.objects.filter(foodie=request.user, category='loving_it'),
        'all_time_favorites': Favorite.objects.filter(foodie=request.user, category='all_time_favorites')
    }

    return render(request, 'favorites.html', context)

def create_favorite(request, product_id):
    product = Product.objects.get(pk = product_id) 
    form = FavoriteForm(request.POST or None)
        
    if form.is_valid() and request.method == 'POST':
        favorite = form.save(commit=False)
        favorite.foodie = request.user 
        favorite.product = product  
        favorite.save() 
        return HttpResponseRedirect(reverse('favorites:main'))
    
    context = {'form': form, 'product': product}
    return render(request, 'create_favorite.html', context)

def edit_favorite(request, product_id):
    product = Product.objects.get(pk = product_id) 
    form = FavoriteForm(request.POST or None, instance=product)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('favorites:main'))

    context = {'form': form}

    return render(request, 'edit_favorite.html', context)

def delete_favorite(request, product_id):
    product = Product.objects.get(pk = product_id) 
    product.delete()
    return HttpResponseRedirect(reverse('favorites:main'))

def user_favorites(request, user_id):
    profile_user = User.objects.get(pk = user_id)
    favorites = Favorite.objects.filter(foodie=profile_user)

    # Filter berdasarkan kategori
    want_to_try = favorites.filter(category='craving')
    loving_it = favorites.filter(category='cant_get_enough')
    all_time_favorites = favorites.filter(category='all_time_favorites')

    context = {
        'profile_user': profile_user,
        'want_to_try': want_to_try,
        'loving_it': loving_it,
        'all_time_favorites': all_time_favorites,
    }
    return render(request, 'favorites/profile_favorites.html', context)