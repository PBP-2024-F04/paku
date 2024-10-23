from django.shortcuts import render, redirect
from django import forms
from .models import Promo
from products.models import Product
from .forms import PromoForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def main(request):
    promos = Promo.objects.filter(user=request.user)  # Ambil semua promo yang dibuat oleh user
    return render(request, 'promos.html', {'promos': promos})

def get_user_products(request):
    user = request.user
    if request.is_ajax() and user.is_authenticated:
        # Ambil product milik user
        products = Product.objects.filter(user=user)
        product_data = [{'id': product.id, 'name': product.name} for product in products]
        return JsonResponse({'products': product_data})
    return JsonResponse({'error': 'Unauthorized access'}, status=403)

@login_required
def add_promo(request):
    if request.method == 'POST':
        form = PromoForm(request.POST)
        if form.is_valid():
            promo = form.save(commit=False)
            promo.user = request.user  # Menyimpan user yang sedang login sebagai pemilik promo
            promo.save()
            return redirect('user_promos')  # Redirect ke halaman semua promo user setelah berhasil menambah promo
    else:
        form = PromoForm()

    return render(request, 'promos/add_promo.html', {'form': form})
