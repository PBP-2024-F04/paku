from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from products.forms import ProductForm
from products.models import Product
from django.db.models import Q
import json

# Show all products from database
@login_required(login_url='/accounts/login')
def main(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')

    dataset_products = Product.objects.filter(user__isnull=True)
    user_products = Product.objects.filter(user__isnull=False)

    if query:
        dataset_products = dataset_products.filter(Q(product_name__icontains=query))
        user_products = user_products.filter(Q(product_name__icontains=query))
    
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

def products_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def product_by_id_json(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def create_product_flutter(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({"status": "error", "message": "User not authenticated"}, status=401)

        if not hasattr(request.user, 'role') or request.user.role != 'Merchant':
            return JsonResponse({"status": "error", "message": "Access denied. Only merchants can add products."}, status=403)
        
        data = json.loads(request.body)
        new_product = Product.objects.create(
            user=request.user,
            product_name=data["productName"],
            restaurant=request.user.merchantprofile.restaurant_name,
            price=int(data["price"]),
            description=data["description"],
            category=data["category"],
        )

        new_product.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

@login_required(login_url='/accounts/login')
@csrf_exempt
def edit_product_flutter(request, id):
    try:
        if request.method == "POST":
            data = json.loads(request.body)

            # Cari produk berdasarkan ID
            try:
                product = Product.objects.get(id=id)
            except Product.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Produk tidak ditemukan."}, status=404)

            product.product_name = data.get("productName", product.product_name)
            product.price = data.get("price", product.price)
            product.description = data.get("description", product.description)
            product.category = data.get("category", product.category)
            product.save()

            return JsonResponse({"status": "success", "message": "Produk berhasil diperbarui!"})
        else:
            return JsonResponse({"status": "error", "message": "Metode tidak diizinkan."}, status=405)
    except Exception as e:
        print(f"Kesalahan: {e}")
        return JsonResponse({"status": "error", "message": "Terjadi kesalahan."}, status=500)

@login_required(login_url='/accounts/login')  
def my_products_flutter(request):
    products = Product.objects.filter(user=request.user).values(
        'id', 'product_name', 'price', 'description', 'category'
    )
    return JsonResponse({'success': True, 'products': list(products)})