from django.shortcuts import render, redirect
from django import forms
from .models import Promo
from products.models import Product
from .forms import PromoForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='/accounts/login')
def main(request):
    promos = Promo.objects.all()
    return render(request, 'promos.html', {'promos': promos, 'user' : request.user})

def my_promos(request):
    promos = Promo.objects.filter(user=request.user) 
    return render(request, 'promos.html', {'promos': promos, 'user' : request.user})

def get_user_products(request):
    user = request.user
    if request.is_ajax() and user.is_authenticated:
        products = Product.objects.filter(user=user)
        product_data = [{'id': product.id, 'name': product.name} for product in products]
        return JsonResponse({'products': product_data})
    return JsonResponse({'error': 'Unauthorized access'}, status=403)

def add_promo(request):
    if request.method == 'POST':
        promo_form = PromoForm(request.POST)

        if promo_form.is_valid():
            promo = promo_form.save(commit=False)
            promo.user = request.user
            promo.save()

            messages.success(request, "Your post has been successfully created!")
            return redirect('promo:my_promos')

    post_form = PromoForm()

    return render(request, 'add_promo.html', {'form': post_form,})

def edit_promo(request):
    pass

def delete_promo(request):
    pass