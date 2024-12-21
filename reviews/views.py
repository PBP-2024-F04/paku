import json
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Review
from .forms import ReviewForm
from products.models import Product

# show main review
def main(request):
    all_reviews = Review.objects.all()
    
    if request.user.is_authenticated:
        my_reviews = Review.objects.filter(user=request.user)
        
        if request.user.role == 'Merchant':
            merchant_products = Product.objects.filter(user=request.user)
            merchant_reviews = Review.objects.filter(product__in=merchant_products)
        else:
            merchant_reviews = None
    else:
        my_reviews = None
        merchant_reviews = None

    print("All Reviews:", all_reviews)
    print("My Reviews:", my_reviews)
    print("Merchant Reviews:", merchant_reviews)
    
    return render(request, 'reviews.html', {
        'all_reviews': all_reviews,
        'my_reviews': my_reviews,
        'merchant_reviews': merchant_reviews,
    })

def show_json(request):
    data = Review.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, id):
    data = Review.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def get_reviews_flutter(request):
    reviews = Review.objects.all().order_by('-created_at')
    data = [
        {
            "id": review.id,
            "user": {
                "role": review.user.role,
                "display_name":
                    review.user.foodieprofile.full_name
                    if review.user.role == "Foodie" else
                    review.user.merchantprofile.restaurant_name,
                "username": review.user.username,
            },
            "product": {
                "product_name": review.product.product_name,
                "restaurant": review.product.restaurant,
                "price": review.product.price,
            },
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at,
            "updated_at": review.updated_at,
        }
        for review in reviews
    ]
    return JsonResponse(data, content_type="application/json", safe=False)

@login_required(login_url='/accounts/login')
def get_my_reviews_flutter(request):
    my_reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    data = [
        {
            "id": review.id,
            "user": {
                "role": review.user.role,
                "display_name":
                    review.user.foodieprofile.full_name
                    if review.user.role == "Foodie" else
                    review.user.merchantprofile.restaurant_name,
                "username": review.user.username,
            },
            "product": {
                "product_name": review.product.product_name,
                "restaurant": review.product.restaurant,
                "price": review.product.price,
            },
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at,
            "updated_at": review.updated_at,
        }
        for review in my_reviews
    ]
    return JsonResponse(data, content_type="application/json", safe=False)

# Show reviews for a specific product
def product_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    return render(request, 'product_review.html', {'product': product, 'reviews': reviews, 'star_range': range(1, 6)})

# Create a new review
@login_required(login_url='/accounts/login')
def create_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return JsonResponse({'success': True, 'review_id': review.id, 'message': 'Review created successfully!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ReviewForm()

    ratings = [1, 2, 3, 4, 5]
    
    return render(request, 'create_review.html', {'form': form, 'product': product, 'ratings': ratings})

# Edit an existing review
@login_required(login_url='/accounts/login')
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    if request.user != review.user:
        return JsonResponse({'success': False, 'message': 'Unauthorized access.'}, status=403)  # Prevent editing if not the owner
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Review updated successfully!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ReviewForm(instance=review)

    ratings = [1, 2, 3, 4, 5]
    
    return render(request, 'create_review.html', {'form': form, 'product': review.product, 'ratings': ratings})

# Delete a review
@login_required(login_url='/accounts/login')
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    if request.user == review.user:
        review.delete()
    
    return HttpResponseRedirect(reverse('reviews:main'))

def product_review_json(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    data = [
        {
            "id": review.id,
            "user": {
                "role": review.user.role,
                "display_name":
                    review.user.foodieprofile.full_name
                    if review.user.role == "Foodie" else
                    review.user.merchantprofile.restaurant_name,
                "username": review.user.username,
            },
            "product": {
                "product_name": review.product.product_name,
                "restaurant": review.product.restaurant,
                "price": review.product.price,
            },
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at,
            "updated_at": review.updated_at,
        }
        for review in reviews
    ]
    return JsonResponse(data, content_type="application/json", safe=False)

@csrf_exempt
@require_POST
@login_required(login_url='/accounts/login')
def create_review_json(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    data = json.loads(request.body)
    review_form = ReviewForm(data)

    if review_form.is_valid():
        review = review_form.save(commit=False)
        review.product = product
        review.user = request.user
        review.save()

        return JsonResponse({
            "success": True,
            "message": "Reviewed!"
        }, status=200)

    return JsonResponse({
        "success": False,
        "errors": review_form.errors,
    }, status=400)

@csrf_exempt
@require_POST
@login_required(login_url='/accounts/login')
def edit_review_json(request, review_id):
    data = json.loads(request.body)

    instance = get_object_or_404(Review, pk=review_id, user=request.user)

    review_form = ReviewForm(data, instance=instance)

    if review_form.is_valid():
        review: Review = review_form.save(commit=False)
        review.is_edited = True
        review.save()

        return JsonResponse({
            "success": True,
            "message": "Edited!",
        }, status=200)

    return JsonResponse({
        "success": False,
        "errors": review_form.errors,
    }, status=400)

@csrf_exempt
@require_POST
@login_required(login_url='/accounts/login')
def delete_review_json(request, review_id):
    instance = get_object_or_404(Review, pk=review_id, user=request.user)

    instance.delete()

    return JsonResponse({
        "success": True,
        "message": "Deleted!",
    }, status=200)