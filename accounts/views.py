from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .models import User
from .forms import UserRegistrationForm

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
            form.save()
            messages.success(request, "Your account has been successfully created!")
            return redirect('accounts:login')
    
    form = UserRegistrationForm()
    return render(request, 'register.html', {'form':form})

def home_page(request):
    return render(request, 'home.html', {'user': request.user})
