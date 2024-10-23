from django.shortcuts import render, redirect
from django import forms
from .models import Promo
from products.models import Product
from .forms import PromoForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def main(request):
    return render(request, 'promos.html')

@login_required
def user_promos(request):
    # User sudah dipastikan login
    promos = Promo.objects.filter(user=request.user)  # Ambil semua promo yang dibuat oleh user
    return render(request, 'promos/user_promos.html', {'promos': promos})

def get_user_products(request):
    user = request.user
    if request.is_ajax() and user.is_authenticated:
        # Ambil product milik user
        products = Product.objects.filter(user=user)
        product_data = [{'id': product.id, 'name': product.name} for product in products]
        return JsonResponse({'products': product_data})
    return JsonResponse({'error': 'Unauthorized access'}, status=403)

def create_promo(request):
    if request.method == 'POST':
        form = PromoForm(request.POST)
        if form.is_valid():
            promo = form.save(commit=False)
            promo.user = request.user  
            promo.product_id = request.POST.get('product')  
            promo.save()
            return redirect('promos.html')
    else:
        form = PromoForm()

    return render(request, 'promos/create_promo.html', {'form': form})
