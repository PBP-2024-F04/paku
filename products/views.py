from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from products.forms import ProductForm
from products.models import Product
from django.db.models import Q

# Show all products from database
def main(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')

    dataset_products = Product.objects.filter(user__isnull=True)
    user_products = Product.objects.filter(user__isnull=False)

    if query:
        dataset_products = dataset_products.filter(Q(product_name__icontains=query) | Q(description__icontains=query))
        user_products = user_products.filter(Q(product_name__icontains=query) | Q(description__icontains=query))
    
    if category:
        dataset_products = dataset_products.filter(category__icontains=category)
        user_products = user_products.filter(category__icontains=category)

    products = dataset_products.union(user_products)
    categories = Product.objects.values_list('category', flat=True).distinct()

    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'category_name': category,
        'empty_message': "Tidak ada produk yang sesuai dengan pencarian atau kategori." if not products else "",
    }

    return render(request, 'database_products.html', context)

# Show all logged in merchant's products
@login_required(login_url='/accounts/login')
def my_products(request):
    products = Product.objects.filter(user=request.user)

    context = {
        'products': products,
        'empty_message': 'Anda belum memiliki produk. Silakan tambahkan produk baru.',
    }

    return render(request, 'products.html', context)

# Show a specific product
@login_required(login_url='/accounts/login')
def view_product(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, 'view_product.html', {'product': product})

@csrf_exempt
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

@csrf_exempt
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

@csrf_exempt
@login_required(login_url='/accounts/login')
def delete_product(request, id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=id)
        product.delete()
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)