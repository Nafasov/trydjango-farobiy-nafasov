from django.shortcuts import render, redirect, reverse
# from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth.forms import UserCreationForm
from .form import MyUserCreationForm, MyAuthenticationForm
from django.contrib import messages


def _login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if not user:
            raise ObjectDoesNotExist("User not found")
        login(request, user)
        return redirect("/")
    context ={

    }
    return render(request, 'auth/login.html', context)


def login_view(request):
    if request.user.is_authenticated:
        messages.error(request, 'This is impossible!')
        raise ConnectionError('This is impossible!')
    form = MyAuthenticationForm()
    if request.method == "POST":
        form = MyAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'{user.username} you have successfully logged in!')
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'auth/login-form.html', context)


def logout_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'This is impossible!')
        raise ConnectionError('This is impossible!')
    if request.method == 'POST':
        user = request.user
        logout(request)
        messages.error(request, f'{user.username} you have successfully logged out!')
        return redirect('article:list')
    return render(request, 'auth/logout.html')


def register_view(request):
    if request.user.is_authenticated:
        messages.error(request, 'This is impossible!')
        raise ConnectionError('This is impossible!')
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print("salom")
            return redirect('auth:login')
    context = {
        'form': form
    }
    return render(request, 'auth/register.html', context)
