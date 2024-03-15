from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            new_registered_user = form.save()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(username=email, password=password)
            login(user=user, request=request)
            messages.success(request, "Sign Up Success! Enjoy Shopping")
            return redirect('core:home')
        else:
            messages.error(request, "Sign Up Failed! Try Again")
    else:
        form = RegisterForm(request.POST or None)
    return render(request, 'userauth/Register.html', {
        'form': form,
    })


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already Logged In!")
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user=user)
            messages.success(request, "Logged In! Happy Shopping")
            return redirect('core:home')
        else:
            messages.error(request, "Login Failed! Try Again")
    return render(request, 'userauth/Login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out")
    return redirect('core:home')
