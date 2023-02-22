from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm


def register_user(request):
    if not request.user.is_anonymous:
        return redirect('index')
    page = 'register'
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.name = user.name.title()
            user.save()
            messages.success(request, f'Welcome {user.name}!')
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'core/login-register.html', {
                'page': page,
                'form': form
            })

    return render(request, 'core/login-register.html', {
        'page': page,
        'form': CustomUserCreationForm()
    })


def login_user(request):
    if not request.user.is_anonymous:
        return redirect('index')
    page = 'login'
    if request.method == 'POST':
        email = request.POST['email'].lower()
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        if user is not None:
            messages.success(request, f'Welcome Back, {user.name}!')
            login(request, user)
            return redirect(request.GET['next'] if request.GET.get('next') else 'index')
        else:
            messages.error(request, 'Wrong Email or/and Password')

    return render(request, 'core/login-register.html', {
        'page': page,
    })


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.info(request, 'See you again!')
    return redirect('index')
