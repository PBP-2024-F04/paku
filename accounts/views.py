from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .models import FoodieProfile, User
from .forms import FoodieProfileForm, MerchantProfileForm, UserRegistrationForm

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

    return render(request, 'login.html')

def register_page(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            if user.role == 'Foodie':
                foodie_form = FoodieProfileForm(request.POST)

                if foodie_form.is_valid():
                    foodie: FoodieProfile = foodie_form.save(commit=False)
                    foodie.user = user
                    foodie.save()
                
            if user.role == 'Merchant':
                merchant_form = MerchantProfileForm(request.POST)

                if merchant_form.is_valid():
                    merchant = merchant_form.save(commit=False)
                    merchant.user = user
                    merchant.save()

            messages.success(request, "Your account has been successfully created!")
            return redirect('accounts:login')
    
    form = UserRegistrationForm()
    foodie_form = FoodieProfileForm()
    merchant_form = MerchantProfileForm()

    return render(request, 'register.html', {
        'form': form,
        'foodie_form': foodie_form,
        'merchant_form': merchant_form,
    })

def home_page(request):
    return render(request, 'home.html', {'user': request.user})
