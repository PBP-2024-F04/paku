from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from products.forms import ProductForm
from products.models import Product

# Show all products from database
def main(request):
    dataset_products = Product.objects.filter(user__isnull=True)
    user_products = Product.objects.filter(user__isnull=False)

    products = dataset_products.union(user_products)
    
    return render(request, 'database_products.html', {'products': products})

# Show all logged in merchant's products
@login_required(login_url='/accounts/login')
def my_products(request):
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
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return JsonResponse({'success': True, 'redirect_url': '/products/me/'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ProductForm()
    context = {'form': form}
    return render(request, "create_product.html", context)

@login_required(login_url='/accounts/login')
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ProductForm(instance=product)

    context = {'form': form, 'product': product}
    return render(request, "edit_product.html", context)

@login_required(login_url='/accounts/login')
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    product.delete()
    messages.success(request, "Your product has been successfully deleted!")
    return redirect('products:my_products')

# Show all categories
def view_categories(request):
    categories = Product.objects.values_list('category', flat=True).distinct()
    return render(request, 'view_categories.html', {'categories': categories})

# Show products by category
def products_by_category(request, category_name):
    products = Product.objects.filter(category=category_name)
    context = {
        'products': products,
        'category_name': category_name
    }
    return render(request, 'database_products.html', context)