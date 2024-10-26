from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .models import FoodieProfile, MerchantProfile, User
from .forms import FoodieProfileForm, MerchantProfileForm, UserLoginForm, UserRegistrationForm

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('accounts:home')
        else:
            messages.error(request, "Username or Password does not match")

    form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def register_page(request):
    return render(request, 'register.html')

def register_foodie_page(request):
    form = UserRegistrationForm()
    foodie_form = FoodieProfileForm()

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        foodie_form = FoodieProfileForm(request.POST)

        if form.is_valid() and foodie_form.is_valid():
            user = form.save(commit=False)
            user.role = 'Foodie'
            user.save()

            foodie: FoodieProfile = foodie_form.save(commit=False)
            foodie.user = user
            foodie.save()

            messages.success(request, "Your account has been successfully created!")
            return redirect('accounts:login')

    return render(request, 'register_foodie.html', {
        'form': form,
        'foodie_form': foodie_form,
    })

def register_merchant_page(request):
    form = UserRegistrationForm()
    merchant_form = MerchantProfileForm()

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        merchant_form = MerchantProfileForm(request.POST)

        if form.is_valid() and merchant_form.is_valid():
            user: User = form.save(commit=False)
            user.role = 'Merchant'
            user.save()

            merchant: MerchantProfile = merchant_form.save(commit=False)
            merchant.user = user
            merchant.save()

            messages.success(request, "You account has been successfully created!")
            return redirect('accounts:login')

    return render(request, 'register_merchant.html', {
        'form': form,
        'merchant_form': merchant_form,
    })

def home_page(request):
    if request.user.role == 'Foodie':
        return render(request, 'home_foodie.html', {'user': request.user})
    else:
        return render(request, 'home_merchant.html', {'user': request.user})
