from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from products.forms import ProductForm
from products.models import Product

@login_required(login_url='/accounts/login')
def main(request):
    products = Product.objects.all()

    context = {
        'products' : products,
    }

    return render(request, 'products.html', context)

@login_required(login_url='/accounts/login')
def vieww(request): # blm fix
    products = Product.objects.filter(user=request.user)

    context = {
        'products' : products,
    }

    return render(request, 'products.html', context)

@login_required(login_url='/accounts/login')
def view_product(request):
    product = get_object_or_404(Product, pk=id)
    return render(request, 'products.html', {'product' : product})

@login_required(login_url='/accounts/login')
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product = form.save(commit=False)
        product.user = request.user
        product.save()
        messages.success(request, "Your product has been successfully created!")
        return redirect('products:main')

    context = {'form': form}
    return render(request, "create_product.html", context)

@login_required(login_url='/accounts/login')
def edit_product(request, id):
    product = Product.objects.get(pk = id)
    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('products:main'))

    context = {'form': form}
    return render(request, "edit_product.html", context)

@login_required(login_url='/accounts/login')
def delete_product(request, id):
    product = Product.objects.get(pk = id)
    product.delete()
    return HttpResponseRedirect(reverse('products:main'))