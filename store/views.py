from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm

def category_summary(request):
    categories = Category.objects.all()
    context = {
        "categories": categories,
    }
    return render(request, 'category_summary.html', context )
    

def category(request, foo):
    foo = foo.replace('-', ' ')

    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        context = {
            'products': products, 
            'category': category,
        }
        return render(request, 'category.html', context )
    
    except:
        messages.success(request, (f"Category {foo} doesn't exist"))
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
        
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User has been updated!")
            return redirect('home')
        
        return render(request, "update_user.html", {'user_form':user_form})
    
    else:
        messages.success(request, "You must be logged to acces this page")
        redirect('home')
    return render(request, 'update_user.html', {})

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Password updated")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.error.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {'form':form})

    else:
        messages.success(request, "You must be logged to acces this page")
        redirect('home')

    return render(request, 'update_password.html', {})