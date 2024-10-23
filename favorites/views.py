from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from products.models import Product
from .models import Favorite
from .forms import FavoriteForm

def main(request):
    context = {
        'user': request.user,
        'want_to_try': Favorite.objects.filter(user=request.user, category='want_to_try'),
        'loving_it': Favorite.objects.filter(user=request.user, category='loving_it'),
        'all_time_favorites': Favorite.objects.filter(user=request.user, category='all_time_favorites')
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

def delete_mood(request, product_id):
    product = Product.objects.get(pk = product_id) 
    product.delete()
    return HttpResponseRedirect(reverse('favorites:main'))