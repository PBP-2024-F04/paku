from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from reviews.models import Review
from .models import Favorite
from .forms import FavoriteForm
from accounts.models import User, FoodieProfile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

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
    product = get_object_or_404(Product, pk=product_id)
    existing_favorite = Favorite.objects.filter(foodie=request.user, product=product).first()

    if existing_favorite:
        return redirect('favorites:edit_favorite', favorite_id=existing_favorite.favorite_id)
    
    form = FavoriteForm(request.POST or None)
        
    if form.is_valid() and request.method == 'POST':
        favorite = form.save(commit=False)
        favorite.foodie = request.user 
        favorite.product = product  
        favorite.save() 
        return redirect('favorites:main')
    
    context = {
        'form': form, 
        'product': product,
        'user': request.user,
        'want_to_try': Favorite.objects.filter(foodie=request.user, category='want_to_try'),
        'loving_it': Favorite.objects.filter(foodie=request.user, category='loving_it'),
        'all_time_favorites': Favorite.objects.filter(foodie=request.user, category='all_time_favorites')
    }
    return render(request, 'create_favorite.html', context)

@login_required(login_url='/accounts/login')
def edit_favorite(request, favorite_id):
    favorite = get_object_or_404(Favorite, pk=favorite_id)
    form = FavoriteForm(request.POST or None, instance=favorite)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('favorites:main')

    context = {
        'form': form,
        'favorite': favorite,
        'user': request.user,
        'want_to_try': Favorite.objects.filter(foodie=request.user, category='want_to_try'),
        'loving_it': Favorite.objects.filter(foodie=request.user, category='loving_it'),
        'all_time_favorites': Favorite.objects.filter(foodie=request.user, category='all_time_favorites')
    }

    return render(request, 'edit_favorite.html', context)

@login_required(login_url='/accounts/login')
def delete_favorite(request, favorite_id):
    favorite = get_object_or_404(Favorite, pk=favorite_id) 

    if favorite.foodie != request.user:
        return redirect('favorites:main')
    
    favorite.delete()
    return redirect('favorites:main')

@login_required(login_url='/accounts/login')
def user_favorites(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)
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
    return render(request, 'profile_favorites.html', context)

@login_required(login_url='/accounts/login')
def category_favorites(request, category_name):
    valid_categories = {
        'want_to_try': 'Want to Try',
        'loving_it': 'Loving It',
        'all_time_favorites': 'All Time Favorite'
    }

    if category_name not in valid_categories:
        return render(request, 'category_favorites.html', {'favorites': [], 'error': 'Kategori tidak ditemukan.'})

    favorites = Favorite.objects.filter(foodie=request.user, category=category_name)

    return render(request, 'category_favorites.html', {
        'favorites': favorites,
        'category_name': valid_categories[category_name],
        'category_strip':category_name
    })

def search_results(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(product_name__icontains=query)  # Menyesuaikan pencarian
    return render(request, 'search_results.html', {'products': products, 'query': query})

def create_favorite_ajax(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Ambil produk berdasarkan ID

    if request.method == 'POST':
        category = request.POST.get('category')

        # Buat favorit baru
        favorite = Favorite.objects.create(
            foodie=request.user,
            product=product,
            category=category
        )

        return JsonResponse({'success': True, 'message': 'Favorit berhasil ditambahkan!'})
    
    return JsonResponse({'success': False, 'message': 'Request tidak valid.'}, status=400)