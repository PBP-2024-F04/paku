from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from products.forms import ProductForm
from products.models import Product

# Show all products from database
def main(request):
    products = Product.objects.all()

    context = {
        'products' : products,
    }

    return render(request, 'products.html', context)

# Show all merchant's products who is currently loggd in
@login_required(login_url='/accounts/login')
def view_products(request):
    products = Product.objects.filter(user=request.user)

    context = {
        'products': products,
        'empty_message': 'You dont have any products yet. Please create a new product.',
    }

    return render(request, 'products.html', context)

# Show a specific product
@login_required(login_url='/accounts/login')
def view_product(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, 'view_product.html', {'product': product})

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
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid() and request.method == "POST":
        form.save()
        messages.success(request, "Your product has been successfully updated!")
        return redirect('products:main')

    context = {'form': form, 'product': product}
    return render(request, "edit_product.html", context)

@login_required(login_url='/accounts/login')
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    messages.success(request, "Your product has been successfully deleted!")
    return redirect('products:main')