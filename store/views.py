from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms

def category(request, foo):
    foo = foo.replace('-', ' ')

    try:
        category = Category.object.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products}, {'category': category})
    
    except:
        messages.success(request, ("Category doesn't exist"))
        return redirect('home')


def product(request, pk):
    product = Product.objects.get(id=pk)
                                  
    context = {
        'product':product
    }
    return render(
        request, 'product.html', context,
    )


def home(request):
    products = Product.objects.all()

    context = {
        'products':products
    }
    return render(
        request, 'home.html', context,
    )


def about(request):
    return render(request, 'about.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in"))
            return redirect('home')
        else:
            messages.success(request, ("Wrong username or password, please try again"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out"))
    return redirect('home')


def register_user(request):
        form = SignUpForm()
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(request, ("You have been registered"))
                return redirect('home')
            else:
                messages.success(request, ("Something went wrong, please register again"))
                return redirect('register')
        else:
            return render(request, 'register.html', {'form': form})
        



