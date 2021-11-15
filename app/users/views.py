from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile

from users.forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'User created: {username}. You are now logged in.')
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('base:index')

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'users/profile.html', {'profile': profile})
