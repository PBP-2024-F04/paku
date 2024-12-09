import json
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import FoodieProfile, MerchantProfile, User
from .forms import FoodieProfileForm, MerchantProfileForm, UserLoginForm, UserRegistrationForm

def login_page(request):
    if not request.user.is_anonymous:
        return redirect('accounts:home')

    if request.method == "POST":
        form = UserLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect('accounts:home')

        messages.error(request, "Username or Password does not match")

    form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    auth_logout(request)
    return redirect('main:landing')

def register_page(request):
    if not request.user.is_anonymous:
        return redirect('accounts:home')

    return render(request, 'register.html')

def register_foodie_page(request):
    if not request.user.is_anonymous:
        return redirect('accounts:home')

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
    if not request.user.is_anonymous:
        return redirect('accounts:home')

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

@csrf_exempt
@require_POST
def login(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return JsonResponse({
                "username": user.username,
                "success": True,
                "message": "Login sukses!"
            }, status=200)
        else:
            return JsonResponse({
                "success": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "success": False,
            "message": "Login gagal, periksa kembali email atau kata sandi!"
        }, status=401)

@csrf_exempt
@require_POST
def logout(request):
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "success": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
            "success": False,
            "message": "Logout gagal!"
        }, status=401)

@csrf_exempt
@require_POST
def register_foodie(request):
    data = json.loads(request.body)

    form = UserRegistrationForm(data)
    foodie_form = FoodieProfileForm(data)

    if form.is_valid() and foodie_form.is_valid():
        user = form.save(commit=False)
        user.role = 'Foodie'
        user.save()

        foodie: FoodieProfile = foodie_form.save(commit=False)
        foodie.user = user
        foodie.save()

        return JsonResponse({
            "success": True,
            "username": user.username,
            "message": "Foodie account created successfully!"
        }, status=200)

    return JsonResponse({
        "success": False,
        "errors": form.errors,
    }, status=400)

@csrf_exempt
@require_POST
def register_merchant(request):
    data = json.loads(request.body)

    form = UserRegistrationForm(data)
    merchant_form = MerchantProfileForm(data)

    if form.is_valid() and merchant_form.is_valid():
        user: User = form.save(commit=False)
        user.role = 'Merchant'
        user.save()

        merchant: MerchantProfile = merchant_form.save(commit=False)
        merchant.user = user
        merchant.save()

        return JsonResponse({
            "success": True,
            "username": user.username,
            "message": "Merchant account created successfully!"
        }, status=200)
    
    return JsonResponse({
        "success": False,
        "errors": form.errors,
    }, status=200)

@login_required(login_url='/accounts/login')
def home_page(request):
    if request.user.role == 'Foodie':
        return render(request, 'home_foodie.html', {'user': request.user})
    else:
        return render(request, 'home_merchant.html', {'user': request.user})
