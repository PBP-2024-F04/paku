from django.shortcuts import render, redirect
from django import forms
from .models import Promo
from products.models import Product
from .forms import PromoForm
from django.http import JsonResponse

def main(request):
    return render(request, 'promos.html')

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
            return redirect('promo_success_page')
    else:
        form = PromoForm()

    return render(request, 'promos/create_promo.html', {'form': form})
