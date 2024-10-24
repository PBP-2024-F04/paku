from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Review
from products.models import Product
from .forms import ReviewForm

# Show all reviews + My reviews
def main(request):
    all_reviews = Review.objects.all()
    
    if request.user.is_authenticated:
        my_reviews = Review.objects.filter(user=request.user)
    else:
        my_reviews = None
    
    return render(request, 'reviews.html', {'all_reviews': all_reviews, 'my_reviews': my_reviews})

# Show reviews for a specific product
def product_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    return render(request, 'product_review.html', {'product': product, 'reviews': reviews})

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
            return redirect('reviews:product_review', product_id=product.id)
    else:
        form = ReviewForm()
    return render(request, 'create_review.html', {'form': form, 'product': product})

# Edit an existing review
@login_required(login_url='/accounts/login')
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    if request.user != review.user:
        return redirect('reviews:main')  # Prevent editing if not the owner
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('reviews:product_review', product_id=review.product.id)  # Redirect to the product's reviews
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'create_review.html', {'form': form, 'product': review.product})

# Delete a review
@login_required(login_url='/accounts/login')
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    if request.user == review.user:
        review.delete()
    
    return HttpResponseRedirect(reverse('reviews:main'))
